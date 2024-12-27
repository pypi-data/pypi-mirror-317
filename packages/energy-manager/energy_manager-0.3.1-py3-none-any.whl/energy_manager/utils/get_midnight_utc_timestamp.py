import pytz
from datetime import datetime


def get_midnight_utc_timestamp() -> int:
    """
    Retrieves the Unix timestamp for midnight, UTC, of the current date.

    The function calculates the timestamp corresponding to midnight in Coordinated
    Universal Time (UTC) for the current date by utilizing the system's current
    timestamp and timezone settings to identify the date. It then converts the
    midnight UTC datetime into a Unix timestamp.

    Returns:
        int: The Unix timestamp for midnight, UTC, of the current date.
    """
    current_date = datetime.now()
    midnight_utc = datetime(
        current_date.year
        , current_date.month
        , current_date.day
        , 0, 0, 0, tzinfo=pytz.utc
    )
    midnight_utc_timestamp = int(midnight_utc.timestamp())

    return midnight_utc_timestamp
