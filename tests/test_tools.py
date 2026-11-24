from datetime import datetime

from chat_maf.tools import get_current_time


def test_get_current_time_accepts_timezone():
    result = get_current_time("UTC")

    assert result.endswith("+00:00")
    datetime.fromisoformat(result)


def test_get_current_time_falls_back_for_unknown_timezone():
    assert get_current_time("Not/A-Timezone").endswith("+00:00")
