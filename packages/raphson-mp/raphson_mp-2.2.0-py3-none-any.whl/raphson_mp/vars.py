from __future__ import annotations

import weakref
from contextvars import ContextVar
from sqlite3 import Connection
from typing import TYPE_CHECKING

import jinja2
from aiohttp import web

if TYPE_CHECKING:
    from raphson_mp import auth

APP_JINJA_ENV = web.AppKey("jinja_env", jinja2.Environment)
CONN = web.AppKey("conn", Connection)

"""
Tracks websockets and streaming connections that should be closed when the server shuts down
See: https://docs.aiohttp.org/en/stable/web_advanced.html#websocket-shutdown
"""
CLOSE_RESPONSES = web.AppKey("streams", weakref.WeakSet[web.StreamResponse])

LOCALE: ContextVar[str] = ContextVar("LOCALE")
USER: ContextVar[auth.User | None] = ContextVar("USER")
JINJA_ENV: ContextVar[jinja2.Environment] = ContextVar("JINJA_ENV")
