import hmac
import logging
import time
from collections.abc import Iterable
from sqlite3 import Connection
from weakref import WeakSet, WeakValueDictionary

from aiohttp import WSMsgType, web

from raphson_mp import activity, event
from raphson_mp.auth import User
from raphson_mp.common.control import (
    ClientNext,
    ClientPause,
    ClientPlay,
    ClientPlaying,
    ClientPrevious,
    ClientSubscribe,
    ClientToken,
    FileAction,
    PlayerControlCommand,
    ServerCommand,
    ServerFileChange,
    ServerNext,
    ServerPause,
    ServerPlay,
    ServerPlayed,
    ServerPrevious,
    Topic,
    parse,
    send,
)
from raphson_mp.decorators import route
from raphson_mp.music import Track
from raphson_mp.vars import CLOSE_RESPONSES

_LOGGER = logging.getLogger(__name__)

_BY_ID: WeakValueDictionary[str, web.WebSocketResponse] = WeakValueDictionary()
_SUB_ACTIVITY: WeakSet[web.WebSocketResponse] = WeakSet()

PLAYER_CONTROL_COMMANDS: dict[type[PlayerControlCommand], ServerCommand] = {
    ClientPlay: ServerPlay(),
    ClientPause: ServerPause(),
    ClientPrevious: ServerPrevious(),
    ClientNext: ServerNext(),
}


@route("", method="GET")
async def websocket(request: web.Request, conn: Connection, user: User):
    control_id = request.query.get("id")

    if control_id is None:
        raise web.HTTPBadRequest(reason="missing id")

    # If cookies are set, they may have been used to log in and CSRF is possible. In this case,
    # the client must first provide CSRF token before it is trusted.
    trusted = "Cookie" not in request.headers

    ws = web.WebSocketResponse()

    _BY_ID[control_id] = ws
    request.config_dict[CLOSE_RESPONSES].add(ws)

    await ws.prepare(request)

    async for message in ws:
        if message.type == WSMsgType.TEXT:
            try:
                command = parse(message.data)
                _LOGGER.info("received message %s", command)
            except Exception:
                _LOGGER.warning("failed to parse message %s", message.data, exc_info=True)
                continue

            if not trusted:
                if isinstance(command, ClientToken):
                    if hmac.compare_digest(user.csrf, command.csrf):
                        trusted = True
                    else:
                        _LOGGER.warning("invalid CSRF token")
                else:
                    _LOGGER.info("ignoring command, client needs to send CSRF token first")
                continue

            if isinstance(command, ClientPlaying):
                await activity.set_now_playing(
                    conn, user, control_id, command.track, command.paused, command.position, command.duration
                )
            elif isinstance(command, ClientSubscribe):
                if command.topic == Topic.ACTIVITY:
                    _SUB_ACTIVITY.add(ws)

                    # send current data to the client immediately
                    commands = [
                        *[playing.control_command() for playing in activity.now_playing()],
                        *_initial_history_data(conn),
                        *_initial_file_change_data(conn),
                    ]

                    await send(ws, commands)
            elif isinstance(command, PlayerControlCommand):
                target = _BY_ID.get(command.player_id)
                if target is not None:
                    command_to_send = PLAYER_CONTROL_COMMANDS[type(command)]
                    await send(target, command_to_send)
                else:
                    _LOGGER.warning("unknown player id")
            else:
                _LOGGER.warning("ignoring unsupported command")

    return ws


def _initial_history_data(conn: Connection) -> Iterable[ServerPlayed]:
    result = conn.execute(
        """
        SELECT history.timestamp, user.username, user.nickname, history.track
        FROM history
            LEFT JOIN user ON history.user = user.id
        WHERE history.private = 0
        ORDER BY history.timestamp DESC
        LIMIT 10
        """
    )

    commands: list[ServerPlayed] = []
    for timestamp, username, nickname, relpath in result:
        track = Track.by_relpath(conn, relpath)
        if track is None:
            continue
        commands.append(
            ServerPlayed(played_time=timestamp, username=nickname if nickname else username, track=track.info_dict())
        )
    return reversed(commands)


def _initial_file_change_data(conn: Connection):
    result = conn.execute(
        f"""
        SELECT timestamp, action, track, username, nickname
        FROM scanner_log LEFT JOIN user ON user = user.id
        ORDER BY timestamp DESC
        LIMIT 10
        """
    )

    return reversed(
        [
            ServerFileChange(
                change_time=change_time,
                action=FileAction(action),
                track=track,
                username=nickname if nickname else username,
            )
            for change_time, action, track, username, nickname in result
        ]
    )


async def broadcast_playing(event: event.NowPlayingEvent) -> None:
    await send(_SUB_ACTIVITY, event.now_playing.control_command())


async def broadcast_history(event: event.TrackPlayedEvent):
    await send(
        _SUB_ACTIVITY,
        ServerPlayed(
            username=event.user.nickname if event.user.nickname else event.user.username,
            played_time=event.timestamp,
            track=event.track.info_dict(),
        ),
    )


async def broadcast_file_change(event: event.FileChangeEvent):
    username = None
    if event.user:
        username = event.user.nickname if event.user.nickname else event.user.username
    await send(
        _SUB_ACTIVITY,
        ServerFileChange(change_time=int(time.time()), action=event.action, track=event.track, username=username),
    )


event.subscribe(event.NowPlayingEvent, broadcast_playing)
event.subscribe(event.TrackPlayedEvent, broadcast_history)
event.subscribe(event.FileChangeEvent, broadcast_file_change)
