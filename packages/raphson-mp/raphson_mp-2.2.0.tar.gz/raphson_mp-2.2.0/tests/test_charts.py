from raphson_mp import charts, i18n
from raphson_mp.vars import LOCALE


def test_data():
    LOCALE.set(i18n.FALLBACK_LOCALE)
    for period in charts.StatsPeriod:
        for chart in charts.get_data(period):
            assert chart["title"]
