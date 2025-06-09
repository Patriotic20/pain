from datetime import datetime, timedelta, timezone


def _generate_ranges(
    start_time: float, end_time: float, interval_minutes: float
) -> list[dict[str, str]]:
    if not (0 < interval_minutes <= 1440):
        raise ValueError("Interval minutes must be between 0 and 1440")
    if not (0 <= start_time < 24 and 0 <= end_time <= 24):
        raise ValueError("Times must be between 0 and 24 hours")
    if start_time >= end_time:
        raise ValueError("start_time must be before end_time")

    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    start_hour = int(start_time)
    start_minute = int((start_time - start_hour) * 60)
    start = today.replace(hour=start_hour, minute=start_minute)

    end_hour = int(end_time)
    end_minute = int((end_time - end_hour) * 60)
    end = today.replace(hour=end_hour, minute=end_minute)

    interval = timedelta(minutes=interval_minutes)
    current = start
    ranges = []
    while current + interval <= end:
        ranges.append(
            {
                "start_time": current.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": (current + interval).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        current += interval
    return ranges


def time_string_to_float(time_str: str) -> float:
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return round(dt.hour + dt.minute / 60, 2)
