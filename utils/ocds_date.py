from datetime import datetime


def ocds_datetime() -> str:
    """OCDS makes use of ISO8601 date-times."""
    return (datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%SZ')


def ocds_date_to_datetime(str_datetime: str):
    return datetime.strptime(str_datetime, "%Y-%m-%dT%H:%M:%SZ")
