import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from sqlite3 import Connection

from raphson_mp import db, event, metadata, music, settings
from raphson_mp.auth import User
from raphson_mp.common.control import FileAction

log = logging.getLogger(__name__)


async def scan_playlists(conn: Connection) -> set[str]:
    """
    Scan playlist directories, add or remove playlists from the database
    where necessary.
    """
    paths_db = {row[0] for row in conn.execute("SELECT path FROM playlist").fetchall()}
    paths_disk = {p.name for p in settings.music_dir.iterdir() if p.is_dir() and not music.is_trashed(p)}

    add_to_db: list[tuple[str]] = []
    remove_from_db: list[tuple[str]] = []

    for path in paths_db:
        if path not in paths_disk:
            log.info("Going to delete playlist: %s", path)
            remove_from_db.append((path,))

    for path in paths_disk:
        if path not in paths_db:
            log.info("New playlist: %s", path)
            add_to_db.append((path,))

    if add_to_db or remove_from_db:

        def thread():
            with db.connect() as writable_conn:
                writable_conn.executemany("INSERT INTO playlist (path) VALUES (?)", add_to_db)
                writable_conn.executemany("DELETE FROM playlist WHERE path=?", remove_from_db)

        await asyncio.to_thread(thread)

    return paths_disk


@dataclass
class QueryParams:
    main_data: dict[str, str | int | None]
    artist_data: list[dict[str, str]]
    tag_data: list[dict[str, str]]


async def query_params(relpath: str, path: Path) -> QueryParams | None:
    """
    Create dictionary of track metadata, to be used as SQL query parameters
    """
    meta = await metadata.probe(path)

    if not meta:
        return None

    main_data: dict[str, str | int | None] = {
        "path": relpath,
        "duration": meta.duration,
        "title": meta.title,
        "album": meta.album,
        "album_artist": meta.album_artist,
        "track_number": meta.track_number,
        "year": meta.year,
        "lyrics": meta.lyrics,
        "video": meta.video,
    }
    artist_data = [{"track": relpath, "artist": artist} for artist in meta.artists]
    tag_data = [{"track": relpath, "tag": tag} for tag in meta.tags]

    return QueryParams(main_data, artist_data, tag_data)


async def scan_track(
    conn: Connection, user: User | None, playlist_name: str, track_path: Path, track_relpath: str
) -> bool:
    """
    Scan single track.
    Returns: Whether track exists (False if deleted)
    """
    await asyncio.sleep(0)  # yield to event loop

    if not track_path.exists():
        log.info("Deleted: %s", track_relpath)

        def thread():
            with db.connect() as writable_conn:
                writable_conn.execute("DELETE FROM track WHERE path=?", (track_relpath,))

        await asyncio.to_thread(thread)
        await event.fire(event.FileChangeEvent(conn, FileAction.DELETE, track_relpath, user))
        return False

    row = conn.execute("SELECT mtime FROM track WHERE path=?", (track_relpath,)).fetchone()
    db_mtime = row[0] if row else None
    file_mtime = int(track_path.stat().st_mtime)

    # Track does not yet exist in database
    if db_mtime is None:
        log.info("New track, insert: %s", track_relpath)
        params = await query_params(track_relpath, track_path)
        if not params:
            log.warning("Skipping due to metadata error")
            return False

        def thread():
            with db.connect() as writable_conn:
                writable_conn.execute("BEGIN")
                writable_conn.execute(
                    """
                    INSERT INTO track (path, playlist, duration, title, album, album_artist, track_number, year, lyrics, video, mtime)
                    VALUES (:path, :playlist, :duration, :title, :album, :album_artist, :track_number, :year, :lyrics, :video, :mtime)
                    """,
                    {**params.main_data, "playlist": playlist_name, "mtime": file_mtime},
                )
                writable_conn.executemany(
                    "INSERT INTO track_artist (track, artist) VALUES (:track, :artist)", params.artist_data
                )
                writable_conn.executemany("INSERT INTO track_tag (track, tag) VALUES (:track, :tag)", params.tag_data)
                writable_conn.execute("COMMIT")

        await asyncio.to_thread(thread)
        await event.fire(event.FileChangeEvent(conn, FileAction.INSERT, track_relpath, user))
        return True

    if file_mtime != db_mtime:
        log.info(
            "Changed, update: %s (%s to %s)",
            track_relpath,
            datetime.fromtimestamp(db_mtime, tz=timezone.utc),
            datetime.fromtimestamp(file_mtime, tz=timezone.utc),
        )
        params = await query_params(track_relpath, track_path)
        if not params:
            log.warning("Metadata error, delete track from database")

            def thread():
                with db.connect() as writable_conn:
                    writable_conn.execute("DELETE FROM track WHERE path=?", (track_relpath,))

            await asyncio.to_thread(thread)
            await event.fire(event.FileChangeEvent(conn, FileAction.DELETE, track_relpath, user))
            return False

        def thread():
            with db.connect() as writable_conn:
                writable_conn.execute("BEGIN")
                writable_conn.execute(
                    """
                    UPDATE track
                    SET duration=:duration,
                        title=:title,
                        album=:album,
                        album_artist=:album_artist,
                        track_number=:track_number,
                        year=:year,
                        lyrics=:lyrics,
                        video=:video,
                        mtime=:mtime
                    WHERE path=:path
                    """,
                    {**params.main_data, "mtime": file_mtime},
                )
                writable_conn.execute("DELETE FROM track_artist WHERE track=?", (track_relpath,))
                writable_conn.executemany(
                    "INSERT INTO track_artist (track, artist) VALUES (:track, :artist)", params.artist_data
                )
                writable_conn.execute("DELETE FROM track_tag WHERE track=?", (track_relpath,))
                writable_conn.executemany("INSERT INTO track_tag (track, tag) VALUES (:track, :tag)", params.tag_data)
                writable_conn.execute("COMMIT")

        await asyncio.to_thread(thread)
        await event.fire(event.FileChangeEvent(conn, FileAction.UPDATE, track_relpath, user))
        return True

    # Track exists in filesystem and is unchanged
    return True


async def scan_tracks(conn: Connection, user: User | None, playlist_name: str) -> None:
    """
    Scan for added, removed or changed tracks in a playlist.
    """
    log.info("Scanning playlist: %s", playlist_name)
    paths_db: set[str] = set()

    for (track_relpath,) in conn.execute("SELECT path FROM track WHERE playlist=?", (playlist_name,)).fetchall():
        if await scan_track(conn, user, playlist_name, music.from_relpath(track_relpath), track_relpath):
            paths_db.add(track_relpath)

    for track_path in music.list_tracks_recursively(music.from_relpath(playlist_name)):
        track_relpath = music.to_relpath(track_path)
        if track_relpath not in paths_db:
            await scan_track(conn, user, playlist_name, track_path, track_relpath)


def last_change(conn: Connection, playlist: str | None = None):
    if playlist:
        query = "SELECT timestamp FROM scanner_log WHERE playlist = ? ORDER BY id DESC LIMIT 1"
        params = (playlist,)
    else:
        query = "SELECT timestamp FROM scanner_log ORDER BY id DESC LIMIT 1"
        params = ()
    timestamp_row = conn.execute(query, params).fetchone()
    if timestamp_row:
        return datetime.fromtimestamp(timestamp_row[0], timezone.utc)

    return datetime.fromtimestamp(0, timezone.utc)


async def scan(conn: Connection, user: User | None) -> None:
    """
    Main function for scanning music directory structure
    """
    if settings.offline_mode:
        log.info("Skip scanner in offline mode")
        return

    playlists = await scan_playlists(conn)
    for playlist in playlists:
        await scan_tracks(conn, user, playlist)


async def scanner_log(event: event.FileChangeEvent):
    playlist_name = event.track[: event.track.index("/")]
    user_id = event.user.user_id if event.user else None

    def thread():
        with db.connect() as writable_conn:
            writable_conn.execute(
                """
                INSERT INTO scanner_log (timestamp, action, playlist, track, user)
                VALUES (?, ?, ?, ?, ?)
                """,
                (int(time.time()), event.action.value, playlist_name, event.track, user_id),
            )

    await asyncio.to_thread(thread)


event.subscribe(event.FileChangeEvent, scanner_log)
