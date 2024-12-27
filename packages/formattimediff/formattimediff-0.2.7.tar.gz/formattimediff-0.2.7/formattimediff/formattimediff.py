# formattimediff.py
from datetime import datetime, timedelta

def formattimediff(start_time, end_time):
    time_diff = end_time - start_time

    # Extract hours, minutes, and seconds
    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    # Round the seconds
    seconds = round(seconds)

    # Format the output
    formatted_time_diff = f"{int(hours)} Hours, {int(minutes)} Minutes, {int(seconds)} Seconds"
    return formatted_time_diff