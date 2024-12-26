import asyncio
import logging
import time
from sqlite3 import Connection
from typing import Any, cast

from aiohttp import web

from raphson_mp import db, event, i18n, lastfm
from raphson_mp.auth import PrivacyOption, StandardUser, User
from raphson_mp.decorators import route
from raphson_mp.music import Track
from raphson_mp.response import template

log = logging.getLogger(__name__)


@route("", redirect_to_login=True)
async def route_activity(_request: web.Request, _conn: Connection, _user: User):
    """
    Main activity page, showing currently playing tracks and history of
    played tracks and modified files.
    """
    return await template("activity.jinja2")


@route("/files")
async def route_files(_request: web.Request, conn: Connection, _user: User):
    """
    Page with long static list of changed files history, similar to route_all()
    """
    result = conn.execute(
        f"""
        SELECT timestamp, action, playlist, track, nickname, username
        FROM scanner_log LEFT JOIN user ON user = user.id
        ORDER BY timestamp DESC
        LIMIT 2000
        """
    )

    action_translation = {
        "insert": i18n.gettext("Added"),
        "delete": i18n.gettext("Removed"),
        "update": i18n.gettext("Modified"),
    }

    changes = [
        {
            "timestamp": timestamp,
            "time_ago": i18n.format_timedelta(timestamp - int(time.time()), add_direction=True, granularity="minute"),
            "username": nickname if nickname else (username if username else ""),
            "action": action_translation[action],
            "playlist": playlist,
            "track": track,
        }
        for timestamp, action, playlist, track, nickname, username in result
    ]

    return await template("activity_files.jinja2", changes=changes)


@route("/all")
async def route_all(_request: web.Request, conn: Connection, _user: User):
    """
    Page with long static list of playback history, similar to route_files()
    """
    result = conn.execute(
        """
        SELECT history.timestamp, user.username, user.nickname, history.playlist, history.track, track.path IS NOT NULL
        FROM history
            LEFT JOIN user ON history.user = user.id
            LEFT JOIN track ON history.track = track.path
        ORDER BY history.timestamp DESC
        LIMIT 2000
        """
    )
    history: list[dict[str, Any]] = []
    for timestamp, username, nickname, playlist, relpath, track_exists in result:
        if track_exists:
            title = cast(Track, Track.by_relpath(conn, relpath)).metadata().display_title()
        else:
            title = relpath

        history.append(
            {"time": timestamp, "username": nickname if nickname else username, "playlist": playlist, "title": title}
        )

    return await template("activity_all.jinja2", history=history)


@route("/played", method="POST")
async def route_played(request: web.Request, conn: Connection, user: User):
    """
    Route to submit an entry to played tracks history, optionally also
    scrobbling to last.fm. Used by web music player and also by offline
    sync to submit many previously played tracks.
    POST body:
     - track: relpath
     - timestamp: time at which track met played conditions (roughly)
     - csrf: csrf token (ignored in offline mode)
    """
    if user.privacy == PrivacyOption.HIDDEN:
        log.info("Ignoring because privacy==hidden")
        raise web.HTTPNoContent()

    json = await request.json()

    track = Track.by_relpath(conn, cast(str, json["track"]))
    if track is None:
        log.warning("skipping track that does not exist: %s", cast(str, json["track"]))
        raise web.HTTPNoContent()

    timestamp = int(cast(str, json["timestamp"]))
    private = user.privacy == PrivacyOption.AGGREGATE

    if not private:
        await event.fire(event.TrackPlayedEvent(user, timestamp, track))

    def thread():
        with db.connect() as writable_conn:
            writable_conn.execute(
                """
                INSERT INTO history (timestamp, user, track, playlist, private)
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, user.user_id, track.relpath, track.playlist, private),
            )

    await asyncio.to_thread(thread)

    # last.fm requires track length to be at least 30 seconds
    if not private and track.metadata().duration >= 30:
        lastfm_key = lastfm.get_user_key(cast(StandardUser, user))
        if lastfm_key:
            meta = track.metadata()
            await lastfm.scrobble(lastfm_key, meta, timestamp)

    raise web.HTTPNoContent()
