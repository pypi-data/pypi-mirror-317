import asyncio
import importlib
import inspect
import logging
import os
import signal
import weakref
from collections.abc import Awaitable, Callable
from enum import Enum
from sqlite3 import Connection
from typing import Final

import jinja2
from aiohttp import web
from aiohttp.typedefs import Middleware
from attr import dataclass

from raphson_mp import cache, cleanup, db, i18n, middlewares, scanner, settings
from raphson_mp.decorators import Route
from raphson_mp.dev_reload import observe_changes, restart
from raphson_mp.util import log_duration
from raphson_mp.vars import APP_JINJA_ENV, CLOSE_RESPONSES, CONN

_LOGGER = logging.getLogger(__name__)


class RoutesContext(Enum):
    ALWAYS = None
    ONLINE = "online"
    OFFLINE = "offline"


@dataclass
class RoutesModule:
    name: str
    prefix: str | None
    context: RoutesContext


ROUTES_MODULES: list[RoutesModule] = [
    RoutesModule("account", "/account", RoutesContext.ONLINE),
    RoutesModule("activity_offline", "/activity", RoutesContext.OFFLINE),
    RoutesModule("activity", "/activity", RoutesContext.ONLINE),
    RoutesModule("auth", "/auth", RoutesContext.ALWAYS),
    RoutesModule("control", "/control", RoutesContext.ONLINE),
    RoutesModule("dislikes", "/dislikes", RoutesContext.ONLINE),
    RoutesModule("download", "/download", RoutesContext.ONLINE),
    RoutesModule("export", "/export", RoutesContext.ONLINE),
    RoutesModule("files", "/files", RoutesContext.ONLINE),
    RoutesModule("games", "/games", RoutesContext.ALWAYS),
    RoutesModule("info", "/info", RoutesContext.ALWAYS),
    RoutesModule("lastfm", "/lastfm", RoutesContext.ONLINE),
    RoutesModule("metrics", "/metrics", RoutesContext.ONLINE),
    RoutesModule("news", "/news", RoutesContext.ONLINE),
    RoutesModule("offline", "/offline", RoutesContext.OFFLINE),
    RoutesModule("player", "/player", RoutesContext.ALWAYS),
    RoutesModule("playlist", "/playlist", RoutesContext.ALWAYS),
    RoutesModule("radio", "/radio", RoutesContext.ALWAYS),
    RoutesModule("root", None, RoutesContext.ALWAYS),
    RoutesModule("share", "/share", RoutesContext.ONLINE),
    RoutesModule("static", "/static", RoutesContext.ALWAYS),
    RoutesModule("stats", "/stats", RoutesContext.ONLINE),
    RoutesModule("track_offline", "/track", RoutesContext.OFFLINE),
    RoutesModule("track", "/track", RoutesContext.ONLINE),
    RoutesModule("tracks", "/tracks", RoutesContext.ALWAYS),
    RoutesModule("users", "/users", RoutesContext.ONLINE),
]


class TaskScheduler:
    MAINTENANCE_INTERVAL: Final = 1800
    conn: Connection

    def __init__(self, conn: Connection, app: web.Application):
        self.conn = conn
        app.on_startup.append(self.on_startup)

    async def on_startup(self, _app: web.Application):
        asyncio.create_task(self.run_periodically(self.maintenance, self.MAINTENANCE_INTERVAL))

    async def run_periodically(
        self, func: Callable[[], Awaitable[None]], interval: float, start_immediately: bool = False
    ):
        if not start_immediately:
            await asyncio.sleep(interval)
        while True:
            await asyncio.gather(asyncio.sleep(interval), func())

    @log_duration
    async def maintenance(self):
        await scanner.scan(self.conn, None)
        await cleanup.cleanup()
        await cache.cleanup()


class Server:
    SHUTDOWN_TIMEOUT: int = 5
    dev: bool
    app: web.Application
    should_restart: bool = False
    conn: Connection

    def __init__(self, dev: bool, enable_tasks: bool = False, enable_profiler: bool = False):
        self.dev = dev
        middleware_list: list[Middleware] = [middlewares.unhandled_error, middlewares.proxy_fix, middlewares.auth_error]
        if enable_profiler:
            middleware_list.append(middlewares.profiler)
        self.app = web.Application(
            middlewares=middleware_list,
            client_max_size=1024**3,
        )

        # Database
        self.conn = db.connect(read_only=True).conn
        self.app[CONN] = self.conn
        cache.open_conn()

        async def close_db(_app: web.Application):
            self.conn.close()
            cache.close_conn()

        self.app.on_cleanup.append(close_db)

        # Close streaming connections when the server shuts down
        self.app[CLOSE_RESPONSES] = weakref.WeakSet()

        async def close_responses(app: web.Application):
            for response in app[CLOSE_RESPONSES]:
                _LOGGER.info("force closing: %s", response)
                if isinstance(response, web.WebSocketResponse):
                    _LOGGER.info("closing websocket: %s", response)
                    await response.close()
                else:
                    _LOGGER.info("cancelling request task: %s", response)
                    task = response.task
                    if task:
                        task.cancel()

        self.app.on_shutdown.append(close_responses)

        self._setup_jinja()

        self._register_routes()

        if enable_tasks:
            TaskScheduler(self.conn, self.app)

        async def shutdown_log(_app: web.Application):
            _LOGGER.info("shutting down (waiting up to %s seconds to finish existing requests)", self.SHUTDOWN_TIMEOUT)

        self.app.on_shutdown.append(shutdown_log)

    def _setup_jinja(self):
        jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader("raphson_mp"),
            autoescape=True,
            enable_async=True,
            auto_reload=self.dev,
            undefined=jinja2.StrictUndefined,
        )
        i18n.install_jinja2_extension(jinja_env)
        self.app[APP_JINJA_ENV] = jinja_env

    def _register_routes(self):
        current_context = [RoutesContext.ALWAYS]
        if settings.offline_mode:
            current_context.append(RoutesContext.OFFLINE)
        else:
            current_context.append(RoutesContext.ONLINE)

        for module in ROUTES_MODULES:
            if module.context in current_context:
                _LOGGER.debug("registering routes: %s", module.name)
                self._register_routes_module(module)
            else:
                _LOGGER.debug("skip registering routes: %s", module.name)

    def _register_routes_module(self, module: RoutesModule):
        python_module = importlib.import_module("raphson_mp.routes." + module.name)
        members: list[tuple[str, Route]] = inspect.getmembers_static(
            python_module, lambda member: isinstance(member, Route)
        )
        if module.prefix is None:
            self.app.add_routes([member[1].routedef for member in members])
        else:
            subapp = web.Application()
            subapp.add_routes([member[1].routedef for member in members])
            self.app.add_subapp(module.prefix, subapp)

    def _start_dev(self):
        _LOGGER.info("running in development mode")

        async def on_change():
            self.should_restart = True
            signal.raise_signal(signal.SIGINT)

        async def on_startup(_app: web.Application):
            asyncio.create_task(observe_changes(on_change))

            asyncio.get_running_loop().slow_callback_duration = 0.05
            asyncio.get_running_loop().set_debug(True)

        self.app.on_startup.append(on_startup)

        async def no_cache(_request: web.Request, response: web.StreamResponse) -> None:
            response.headers["Cache-Control"] = "no-cache"

        self.app.on_response_prepare.append(no_cache)

    def start(self, host: str, port: int):
        if self.dev:
            self._start_dev()

        _LOGGER.info("starting web server on http://%s:%s", host, port)
        web.run_app(
            self.app,
            host=host,
            port=port,
            print=None,
            access_log_format=settings.access_log_format,
            handler_cancellation=True,
            shutdown_timeout=self.SHUTDOWN_TIMEOUT,
        )

        if self.should_restart:
            os.putenv("MUSIC_HAS_RELOADED", "1")
            restart()
