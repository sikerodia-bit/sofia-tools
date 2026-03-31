"""
DateTime tool — pure Python, no Docker needed.
Handles current time/date in any timezone and duration calculations.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from tools.models import Tool

TOOL = Tool(
    name="get_datetime",
    description=(
        "Get the current date and time, optionally in a specific timezone. "
        "Use this whenever the user asks about the current time, date, day of week, "
        "or how long until/since a specific date."
    ),
    parameters={
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": (
                    "IANA timezone name, e.g. 'America/Santo_Domingo', 'UTC', "
                    "'America/New_York'. Defaults to America/Santo_Domingo."
                ),
            },
            "target_date": {
                "type": "string",
                "description": (
                    "Optional ISO date string (YYYY-MM-DD) to calculate time until/since."
                ),
            },
        },
        "required": [],
    },
    requires_network=False,
    needs_docker=False,
    timeout_seconds=5,
)


async def run(params: dict) -> str:
    tz_name = params.get("timezone", "America/Santo_Domingo")
    target_date = params.get("target_date")

    try:
        tz = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo("America/Santo_Domingo")
        tz_name = "America/Santo_Domingo (fallback — unknown timezone requested)"

    now = datetime.now(tz)
    result_lines = [
        f"Current time in {tz_name}:",
        f"  Date: {now.strftime('%A, %B %d, %Y')}",
        f"  Time: {now.strftime('%I:%M %p')} ({now.strftime('%H:%M')} 24h)",
        f"  Day:  {now.strftime('%A')}",
        f"  UTC offset: {now.strftime('%z')}",
    ]

    if target_date:
        try:
            target = datetime.fromisoformat(target_date).replace(tzinfo=tz)
            delta = target - now
            days = delta.days
            if days > 0:
                result_lines.append(f"\nTime until {target_date}: {days} days")
            elif days < 0:
                result_lines.append(f"\nTime since {target_date}: {abs(days)} days ago")
            else:
                result_lines.append(f"\n{target_date} is today.")
        except ValueError:
            result_lines.append(f"\nCould not parse target_date: {target_date}")

    return "\n".join(result_lines)
