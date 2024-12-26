"""Package containing utility modules that perform specific tasks."""

# Standard library imports
import traceback


def format_exception_info(exception: Exception):
    """Returns the exception stack trace in the form of a string as it is displayed in the shell.

    Arguments:
        exception -- the exception to format.
    """
    info = type(exception), exception, exception.__traceback__
    fmt_info = traceback.format_exception(*info)
    return "".join(fmt_info)


def format_time(val: int, word: str):
    """(12, 'second') -> '12 seconds '."""
    return f"{val} {word}{'s' * int(val != 1)} " * bool(val)


def format_seconds(seconds: int):
    """Formats the number of seconds as hours, minutes, seconds.

    E.g. 3777 -> '1 hour 2 minutes 57 seconds'
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    hours = format_time(hours, "hour")
    minutes = format_time(minutes, "minute")
    seconds = format_time(seconds, "second")
    return hours + minutes + seconds
