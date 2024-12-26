from __future__ import annotations

import asyncio
from abc import ABC
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from sqlite3 import Connection
from typing import TYPE_CHECKING, TypeVar, cast

from multidict import MultiDict

from raphson_mp.auth import User
from raphson_mp.common.control import FileAction
from raphson_mp.music import Track

if TYPE_CHECKING:
    from raphson_mp.activity import NowPlaying


class Event(ABC):
    pass


@dataclass
class NowPlayingEvent(Event):
    now_playing: NowPlaying


@dataclass
class TrackPlayedEvent(Event):
    user: User
    timestamp: int
    track: Track


@dataclass
class FileChangeEvent(Event):
    conn: Connection
    action: FileAction
    track: str
    user: User | None


_HANDLERS: MultiDict[Callable[[Event], Awaitable[None]]] = MultiDict()


async def fire(event: Event):
    key = type(event).__name__
    await asyncio.gather(*[func(event) for func in _HANDLERS.getall(key)])


T_event = TypeVar("T_event", bound=Event)


def subscribe(event_type: type[T_event], handler: Callable[[T_event], Awaitable[None]]):
    key = event_type.__name__

    async def generic_handler(event: Event):
        await handler(cast(T_event, event))

    _HANDLERS.add(key, generic_handler)
