from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from agent_framework import tool


@tool(
    name="get_current_time",
    description="Get the current date and time in an IANA timezone.",
)
def get_current_time(timezone_name: str = "UTC") -> str:
    try:
        timezone_info = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        timezone_info = ZoneInfo("UTC")
        timezone_name = "UTC"

    return datetime.now(timezone_info).isoformat(timespec="seconds")
