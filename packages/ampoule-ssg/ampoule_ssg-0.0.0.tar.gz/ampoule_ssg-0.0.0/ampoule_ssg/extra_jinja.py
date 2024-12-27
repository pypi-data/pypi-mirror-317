import math
import datetime
import re

def init_filters(site):
    @site.filter("first_paragraph")
    def first_paragraph(value):
        return value.split("\n\n")[0]
    @site.filter("split")
    def split(value, sep, maxsplit=-1):
        return value.split(sep, maxsplit)
    @site.filter("rsplit")
    def rsplit(value, sep, maxsplit=-1):
        return value.rsplit(sep, maxsplit)
    @site.filter("splitlines")
    def splitlines(value, keepends=False):
        return value.splitlines(keepends)
    @site.filter("split_any")
    def split_any(value, separators, maxsplit=-1):
        return re.split("|".join(re.escape(sep) for sep in separators), value, maxsplit)
    @site.filter("split_regex")
    def split_regex(value, pattern, maxsplit=-1):
        return re.split(pattern, value, maxsplit)
    @site.filter("partition")
    def partition(value, sep):
        return value.partition(sep)
    @site.filter("rpartition")
    def rpartition(value, sep):
        return value.rpartition(sep)
    @site.filter("lstrip")
    def lstrip(value, chars=None):
        return value.lstrip(chars)
    @site.filter("rstrip")
    def rstrip(value, chars=None):
        return value.rstrip(chars)
    @site.filter("strip")
    def strip(value, chars=None):
        return value.strip(chars)
    @site.filter("removeprefix")
    def removeprefix(value, prefix):
        return value.removeprefix(prefix)
    @site.filter("removesuffix")
    def removesuffix(value, suffix):
        return value.removesuffix(suffix)
    @site.filter("remove")
    def remove(value, string):
        return value.replace(string, "")
    @site.filter("strftime")
    def strftime(value: datetime.datetime | datetime.date | datetime.time, format_):
        return value.strftime(format_)
    @site.filter("unixtime")
    def unixtime(value: datetime.datetime | datetime.date | datetime.time):
        return round(value.timestamp())
    @site.filter("strptime")
    def strptime(value, format_):
        return datetime.datetime.strptime(value, format_)
    @site.filter("round")
    def round_(value, decimals=0):
        return round(value, decimals)
    @site.filter("floor")
    def floor(value):
        return math.floor(value)
    @site.filter("ceiling")
    def ceiling(value):
        return math.ceil(value)
    @site.filter("units")
    def units(value, decimals=2, scale=1024,
              suffixes=("B", "kiB", "MiB", "GiB", "TiB", "PiB")):
        for unit in suffixes:
            if value < scale:
                break
            value /= scale
        if int(value) == value:
            return int(value) + "\u202f" + unit
        return round(value * 10 ** decimals) / 10 ** decimals + "\u202f" + unit
    @site.filter("conditional")
    def conditional(value, true_value, false_value):
        return true_value if value else false_value
    @site.filter("debug_log_value")
    def debug_log_value(value):
        print(value)
        return value
    @site.filter("harvester_protection")
    def harvester_protection(value):
        return "".join(f"&#x{ord(char):x};" for char in value)
    @site.filter("pretty_number")
    def pretty_number(value, separator="\u202f"):
        return f"{value:,}".replace(",", separator)
    @site.filter("hex")
    def hex_(value):
        return hex(value).removeprefix("0x")
    @site.filter("oct")
    def oct_(value):
        return oct(value).removeprefix("0o")
    @site.filter("bin")
    def bin_(value):
        return bin(value).removeprefix("0b")
    @site.filter("join")
    def join(value, separator=" "):
        return separator.join(value)
    @site.filter("replace")
    def replace(value, old, new):
        return value.replace(old, new)
    @site.filter("file_stat")
    def file_stat(value):
        return value.stat()
    @site.filter("path_cat")
    def path_cat(*value):
        return os.path.join(*value)
    @site.filter("path_dirname")
    def path_dirname(value):
        return os.path.dirname(value)
    @site.filter("path_basename")
    def path_basename(value):
        return os.path.basename(value)
    @site.filter("path_splitext")
    def path_splitext(value):
        return os.path.splitext(value)
    @site.filter("type")
    def type_(value):
        return type(value)
    @site.filter("type_name")
    def type_name(value):
        return type(value).__name__
    @site.filter("each_nth")
    def nth(value, step, start=0):
        return value[start::step]
    @site.filter("key_list")
    def key_list(value):
        return list(value.keys())
    @site.filter("value_list")
    def value_list(value):
        return list(value.values())
    @site.filter("item_list")
    def item_list(value):
        return list(value.items())
    @site.filter("remove_dupes")
    def remove_dupes(value):
        list = []
        for i in value:
            if i not in list:
                list.append(i)
        return list
    @site.filter("percent")
    def percent(value, maximum, decimals=2):
        return round(value * maximum / 100, decimals) + "%"
    @site.filter("percent_of")
    def percent_of(value, total, decimals=2):
        return round(value / total * 100, decimals) + "%"
    @site.filter("permille")
    def permille(value, maximum, decimals=2):
        return round(value * maximum / 1000, decimals) + "‰"
    @site.filter("permille_of")
    def permille_of(value, total, decimals=2):
        return round(value / total * 1000, decimals) + "‰"
    @site.filter("timezone")
    def timezone(value, timezone):
        return value.astimezone(timezone)

def init_tests(site):
    @site.test("instance_of")
    def isinstance_(value, type_):
        return isinstance(value, type_)
    @site.test("only_chars")
    def only_chars(value, chars):
        return set(value).issubset(set(chars))
    @site.test("empty")
    def is_empty(value):
        return not len(value)
    @site.test("not_empty")
    def is_not_empty(value):
        return len(value)
    @site.test("past_date")
    def past_date(value):
        return value < datetime.datetime.now()
    @site.test("future_date")
    def future_date(value):
        return value > datetime.datetime.now()
    @site.test("numeric")
    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    @site.test("startswith")
    def startswith(value, prefix):
        return value.startswith(prefix)
    @site.test("endswith")
    def endswith(value, suffix):
        return value.endswith(suffix)
    @site.test("matches_regex")
    def matches_regex(value, pattern):
        return re.match(pattern, value) is not None
    @site.test("is_callable")
    def is_callable(value):
        return callable(value)
    @site.test("all")
    def all_(value):
        return all(value)
    @site.test("any")
    def any_(value):
        return any(value)
    @site.test("longer_than")
    def longer_than(value, length):
        return len(value) > length
    @site.test("shorter_than")
    def shorter_than(value, length):
        return len(value) < length
    @site.test("weekend")
    def weekend(value):
        return value.weekday() >= 5
    @site.test("weekday")
    def weekday(value):
        return value.weekday() < 5
    @site.test("leap_year")
    def leap_year(value):
        return value.year % 4 == 0 and (value.year % 100 != 0 or value.year % 400 == 0)
    @site.test("almost_equal")
    def almost_equal(value, other, tolerance=1e-6):
        return abs(value - other) < tolerance
