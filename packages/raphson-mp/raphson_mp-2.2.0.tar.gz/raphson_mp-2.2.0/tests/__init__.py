from pathlib import Path

from raphson_mp import logconfig, ratelimit, settings


def setup_module():
    ratelimit.testing = True
    settings.data_dir = Path("./data").resolve()
    settings.music_dir = Path("./music").resolve()
    logconfig.apply_debug()
