import time
from collections.abc import Iterator
from dataclasses import dataclass
from sqlite3 import Connection
from typing import cast

from raphson_mp import event, lastfm
from raphson_mp.auth import StandardUser, User
from raphson_mp.common.control import ServerPlaying
from raphson_mp.music import Track


@dataclass
class NowPlaying:
    player_id: str
    username: str
    update_time: int
    lastfm_update_timestamp: int
    paused: bool
    position: float
    duration: float
    track: Track | None

    def control_command(self) -> ServerPlaying:
        return ServerPlaying(
            player_id=self.player_id,
            username=self.username,
            update_time=self.update_time,
            paused=self.paused,
            position=self.position,
            duration=self.duration,
            track=self.track.info_dict() if self.track else None,
        )


_NOW_PLAYING: dict[str, NowPlaying] = {}


def now_playing() -> Iterator[NowPlaying]:
    current_time = int(time.time())
    for entry in _NOW_PLAYING.values():
        if entry.update_time > current_time - 120:
            yield entry


async def set_now_playing(
    conn: Connection, user: User, player_id: str, relpath: str | None, paused: bool, position: float, duration: float
) -> None:
    track = Track.by_relpath(conn, relpath) if relpath else None

    current_time = int(time.time())
    username = user.nickname if user.nickname else user.username

    now_playing = NowPlaying(player_id, username, current_time, current_time, paused, position, duration, track)
    _NOW_PLAYING[player_id] = now_playing

    if track and not paused and now_playing.lastfm_update_timestamp < current_time - 60:
        user_key = lastfm.get_user_key(cast(StandardUser, user))
        if user_key:
            meta = track.metadata()
            await lastfm.update_now_playing(user_key, meta)
            now_playing.lastfm_update_timestamp = current_time

    await event.fire(event.NowPlayingEvent(now_playing))
