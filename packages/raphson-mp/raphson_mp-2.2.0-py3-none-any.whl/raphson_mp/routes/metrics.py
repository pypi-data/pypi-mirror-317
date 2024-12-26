import functools
import logging

from aiohttp import web

from raphson_mp import activity, db
from raphson_mp.decorators import simple_route

try:
    import prometheus_client
except ImportError:
    prometheus_client = None


_LOGGER = logging.getLogger(__name__)


@simple_route("")
async def route_metrics(_request: web.Request):
    if prometheus_client:
        return web.Response(body=prometheus_client.generate_latest(), content_type="text/plain")
    else:
        _LOGGER.warning("/metrics was queried, but it is unavailable because prometheus_client is not installed")
        raise web.HTTPServiceUnavailable()


if prometheus_client:

    def _active_players():
        return sum(1 for _ in activity.now_playing())

    # Database size
    g_database_size = prometheus_client.Gauge(
        "database_size", "Size of SQLite database files", labelnames=("database",)
    )
    for db_name in db.DATABASE_NAMES:
        g_database_size.labels(db_name).set_function(functools.partial(db.db_size, db_name))

    # Active players
    prometheus_client.Gauge("active_players", "Active players").set_function(_active_players)
