import logging
import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Callable, Protocol, runtime_checkable

from aiohttp import web
from aiohttp.typedefs import Handler

from raphson_mp import auth, i18n
from raphson_mp.vars import APP_JINJA_ENV, CONN, JINJA_ENV, LOCALE, USER


@runtime_checkable
class PublicRouteCallable(Protocol):
    async def __call__(self, request: web.Request, conn: Connection, /) -> web.StreamResponse: ...


@runtime_checkable
class AuthRouteCallable(Protocol):
    async def __call__(self, request: web.Request, conn: Connection, user: auth.User, /) -> web.StreamResponse: ...


RouteCallable = PublicRouteCallable | AuthRouteCallable

_LOGGER = logging.getLogger(__name__)


@dataclass
class Route:
    routedef: web.AbstractRouteDef


def route(
    path: str,
    method: str = "GET",
    public: bool = False,
    require_admin: bool = False,
    skip_csrf_check: bool = False,
    redirect_to_login: bool = False,
) -> Callable[[RouteCallable], Route]:
    assert not (public and require_admin), "cannot be public if admin is required"

    def decorator(route: RouteCallable) -> Route:
        async def handler(request: web.Request) -> web.StreamResponse:
            conn = request.config_dict[CONN]
            # Sometimes (rarely), the persistent read-only connection would have an outdated view of the database. To
            # me this is surprising, but according to the documentation it is expected behaviour:
            # > In WAL mode, SQLite exhibits "snapshot isolation". When a read transaction starts, that reader
            # > continues to see an unchanging "snapshot" of the database file as it existed at the moment in time
            # > when the read transaction started. Any write transactions that commit while the read transaction is
            # > active are still invisible to the read transaction, because the reader is seeing a snapshot of database
            # > file from a prior moment in time.
            # From: https://www.sqlite.org/isolation.html
            # Mostly work around the issue by starting a fresh read transaction for every request handler.
            try:
                conn.execute("COMMIT")
            except sqlite3.OperationalError:
                pass
            conn.execute("BEGIN")
            JINJA_ENV.set(request.config_dict[APP_JINJA_ENV])
            USER.set(None)
            LOCALE.set(i18n.locale_from_request(request))

            if public:
                assert isinstance(route, PublicRouteCallable)
                return await route(request, conn)

            assert isinstance(route, AuthRouteCallable)
            require_csrf = not skip_csrf_check and request.method == "POST"
            user = await auth.verify_auth_cookie(
                request,
                conn,
                require_admin=require_admin,
                require_csrf=require_csrf,
                redirect_to_login=redirect_to_login,
            )
            USER.set(user)
            LOCALE.set(i18n.locale_from_request(request))

            return await route(request, conn, user)

        return Route(web.route(method, path, handler))

    return decorator


def simple_route(
    path: str,
    method: str = "GET",
) -> Callable[[Handler], Route]:
    def decorator(handler: Handler) -> Route:
        return Route(web.route(method, path, handler))

    return decorator
