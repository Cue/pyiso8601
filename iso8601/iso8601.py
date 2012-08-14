"""ISO 8601 date time string parsing

Basic usage:
>>> import iso8601
>>> iso8601.parse_date("2007-01-25T12:00:00Z")
datetime.datetime(2007, 1, 25, 12, 0, tzinfo=<iso8601.iso8601.Utc ...>)
>>>

"""

from datetime import datetime, timedelta, tzinfo

# If re2 is installed use it, instead of re
try:
  import re2 as re
except ImportError:
  import re

__all__ = ["parseDate", "ParseError"]

# Adapted from http://delete.me.uk/2005/03/iso8601.html
ISO8601_REGEX = re.compile(r"(?P<year>[0-9]{4})(-(?P<month>[0-9]{1,2})(-(?P<day>[0-9]{1,2})"
    r"((?P<separator>.)(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})(:(?P<second>[0-9]{2})(\.(?P<fraction>[0-9]+))?)?"
    r"(?P<timezone>Z|(([-+])([0-9]{2}):?([0-9]{2})?))?)?)?)?"
)
TIMEZONE_REGEX = re.compile("(?P<prefix>[+-])(?P<hours>[0-9]{2})\:?(?P<minutes>[0-9]{2})?")

# Yoinked from python docs
ZERO = timedelta(0)



class ParseError(Exception):
  """Raised when there is a problem parsing a date string"""
  pass



class FixedOffset(tzinfo):
  """Fixed offset in hours and minutes from UTC."""


  def __init__(self, offsetHours, offsetMinutes, name):
    self.__offset = timedelta(hours=offsetHours, minutes=offsetMinutes)
    self.__name = name


  def utcoffset(self, dt):
    return self.__offset


  def tzname(self, dt):
    return self.__name


  def dst(self, dt):
    return ZERO


  def __repr__(self):
    return "<FixedOffset %r>" % self.__name

UTC = FixedOffset(0, 0, "UTC")


def parseTimezone(tzstring, default_timezone=UTC):
  """Parses ISO 8601 time zone specs into tzinfo offsets

  """
  if tzstring == "Z":
    return default_timezone
  # This isn't strictly correct, but it's common to encounter dates without
  # timezones so I'll assume the default (which defaults to UTC).
  # Addresses issue 4.
  if tzstring is None:
    return default_timezone
  m = TIMEZONE_REGEX.match(tzstring)
  prefix, hours, minutes = m.groups()
  hours, minutes = int(hours), 0 if not minutes else int(minutes)
  if prefix == "-":
    hours = -hours
    minutes = -minutes
  return FixedOffset(hours, minutes, tzstring)


def getGroups(datestring):
  """Utility function to get the parts of the datestring as a dict."""
  if not isinstance(datestring, basestring):
    raise ParseError("Expecting a string %r" % datestring)
  m = ISO8601_REGEX.match(datestring)
  if not m:
    raise ParseError("Unable to parse date string %r" % datestring)
  return m.groupdict()


def parseDate(datestring, default_timezone=UTC):
  """Parses ISO 8601 dates into datetime objects
  The timezone is parsed from the date string. However it is quite common to
  have dates without a timezone (not strictly correct). In this case the
  default timezone specified in default_timezone is used. This is UTC by
  default.
  """

  groups = getGroups(datestring)
  tz = parseTimezone(groups["timezone"], default_timezone=default_timezone)
  if groups["fraction"] is None:
    groups["fraction"] = 0
  else:
    groups["fraction"] = int(float("0.%s" % groups["fraction"]) * 1e6)
  return datetime(int(groups["year"]), int(groups["month"]), int(groups["day"]),
    int(groups["hour"]), int(groups["minute"]), int(groups["second"]),
    int(groups["fraction"]), tz)


def isTimezoneLessEvent(datestring):
  """Checks if the ISO 8601 event is a timezoneless event."""
  groups = getGroups(datestring)
  return not groups.get('timezone')
