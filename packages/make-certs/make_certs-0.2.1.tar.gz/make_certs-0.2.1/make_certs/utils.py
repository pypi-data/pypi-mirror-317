from datetime import datetime, timezone

RFC5280_UNDEFINED_NOT_AFTER = datetime(
    year=9999,
    month=12,
    day=31,
    hour=23,
    minute=59,
    second=59,
    tzinfo=timezone.utc,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
