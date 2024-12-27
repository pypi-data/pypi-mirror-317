import os
import shutil
import contextlib
import typing
from datetime import datetime

__all__ = [
    "_no_date_constructor",
    "_in_directory",
    "_delete_directory_contents",
    "_parse_date_string",
]


def _no_date_constructor(loader, node):
    """Function to prevent the YAML loader from converting dates, keeping them as strings,
    so they can be parsed in a more lenient way.
    """
    value = loader.construct_scalar(node)
    return value


@contextlib.contextmanager
def _in_directory(directory):
    """Execute a block of code in a different directory.

    :param directory: The directory to change to.
    """
    cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(cwd)


def _delete_directory_contents(directory, dont_delete: typing.Optional[list[str]] = None):
    """Delete all files and directories in a directory recursively,
    but not the directory itself.

    :param directory: The directory to clear.
    :param dont_delete: A list of files and directories to not delete.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file not in dont_delete:
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir not in dont_delete:
                shutil.rmtree(os.path.join(root, dir))


def _parse_date_string(date_string):
    """Parse a date/time string into a datetime object. Supports multiple unambiguous formats.

    :param date_string: The date/time string to parse.
    :return: A datetime object representing the date/time string.
    """
    def split_date_and_time(date_string):
        """Split a date/time string into a date string and a time string.

        :param date_string: The date/time string to split.
        :return: A tuple containing the date and time strings.
        """
        if ":" not in date_string:
            return date_string, "00:00:00"

        elements = date_string.partition(":")
        partition_character = " "
        if " " not in date_string:
            partition_character = "-"
            if "-" not in date_string:
                partition_character = "T"

        date = elements[0].rpartition(partition_character)[0].strip()
        time = elements[0].rpartition(partition_character)[2].strip() + elements[1] + elements[2].strip()
        time = time.removeprefix("T").removesuffix("Z")

        return date, time

    time_formats = [
        # 24-hour ISO
        "%H:%M:%S",
        "%H:%M",
        "%H",
        # Single digit hour
        "-%H:%M:%S",
        "-%H:%M",
        "-%H",
        # 12-hour (AM/PM)
        "%I:%M:%S %p",
        "%I:%M %p",
        "%I %p",
        # Single digit 12-hour
        "-%I:%M:%S %p",
        "-%I:%M %p",
        "-%I %p",
    ]

    date_formats = [
        # ISO formats
        "%Y-%m-%d",
        "%y-%m-%d",
        # European formats
        "%d.%m.%Y",
        "%d.%m.%y",
        # American formats
        "%m/%d/%Y",
        "%m/%d/%y",
        # Text-based European formats
        "%d %B %Y",
        "%d %b %Y",
        "%d %B, %Y",
        "%d %b, %Y",
        # Text-based American formats
        "%B %d %Y",
        "%b %d %Y",
        "%B %d, %Y",
        "%b %d, %Y",
        # ISO weekly calendar
        "%G-W%V-%u",
    ]

    date, time = split_date_and_time(date_string)

    time_object = datetime.min.time()
    date_object = datetime.min.date()

    for time_format in time_formats:
        try:
            time_object = datetime.strptime(time, time_format)
        except ValueError:
            pass
    for date_format in date_formats:
        try:
            date_object = datetime.strptime(date, date_format)
        except ValueError:
            pass

    return datetime.combine(date_object, time_object.time())
