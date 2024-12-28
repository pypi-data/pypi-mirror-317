from typing import List

def generate_daily_timestamps(
        start_timestamp: int,
        hours: int = 24,
) -> List[int]:
    """
    Generates a list of timestamps representing every hour within a specified
    duration, starting from a given timestamp.

    This function creates a list of evenly spaced timestamps, each separated
    by one hour. The amount of timestamps generated is determined by the
    specified number of hours. Each timestamp is represented as an integer,
    indicating the number of seconds since the Unix epoch.

    Args:
        start_timestamp (int): The starting timestamp, in seconds since the Unix
            epoch.
        hours (int): The number of hourly intervals to generate. Defaults to 24.

    Returns:
        List[int]: A list of hourly timestamps starting from the given starting
            timestamp, with the specified number of intervals.
    """
    return [start_timestamp + i * 3600 for i in range(hours)]
