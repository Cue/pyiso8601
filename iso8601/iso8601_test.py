import iso8601
import unittest

from datetime import tzinfo


class ISO8601(unittest.TestCase):
  """Test cases for ISO 8601."""


  def testIso8601Regex(self):
    self.assertIsNotNone(iso8601.ISO8601_REGEX.match("2006-10-11T00:14:33Z"))
    self.assertIsNotNone(iso8601.ISO8601_REGEX.match('2012-07-04T19:00:00'))

    self.assertIsNotNone(iso8601.ISO8601_REGEX.match('2012-07-04T19:00:00-0700'))
    self.assertIsNotNone(iso8601.ISO8601_REGEX.match('2012-07-04T19:00:00-07:00'))
    self.assertIsNotNone(iso8601.ISO8601_REGEX.match('2012-07-04T19:00:00-07'))


  def testTimezoneRegex(self):
    self.assertIsNotNone(iso8601.TIMEZONE_REGEX.match("+01:00"))
    self.assertIsNotNone(iso8601.TIMEZONE_REGEX.match("+00:00"))
    self.assertIsNotNone(iso8601.TIMEZONE_REGEX.match("+01:20"))
    self.assertIsNotNone(iso8601.TIMEZONE_REGEX.match("-01:00"))
    self.assertIsNotNone(iso8601.TIMEZONE_REGEX.match("-01"))
    self.assertIsNotNone(iso8601.TIMEZONE_REGEX.match("+06"))



  def testParseDate(self):
    """Tests parse date tz."""
    d = iso8601.parseDate("2006-10-20T15:34:56Z")
    self.assertEquals(d.year, 2006)
    self.assertEquals(d.month, 10)
    self.assertEquals(d.day, 20)
    self.assertEquals(d.hour, 15)
    self.assertEquals(d.minute, 34)
    self.assertEquals(d.second, 56)
    self.assertEquals(d.tzinfo, iso8601.UTC)


  def testParseDateFraction(self):
    """Tests parse date tz."""
    d = iso8601.parseDate("2006-10-20T15:34:56.123Z")
    self.assertEquals(d.year, 2006)
    self.assertEquals(d.month, 10)
    self.assertEquals(d.day, 20)
    self.assertEquals(d.hour, 15)
    self.assertEquals(d.minute, 34)
    self.assertEquals(d.second, 56)
    self.assertEquals(d.microsecond, 123000)
    self.assertEquals(d.tzinfo, iso8601.UTC)


  def testParseDateFraction2(self):
    """From bug 6"""
    d = iso8601.parseDate("2007-5-7T11:43:55.328Z'")
    self.assertEquals(d.year, 2007)
    self.assertEquals(d.month, 5)
    self.assertEquals(d.day, 7)
    self.assertEquals(d.hour, 11)
    self.assertEquals(d.minute, 43)
    self.assertEquals(d.second, 55)
    self.assertEquals(d.microsecond, 328000)
    self.assertEquals(d.tzinfo, iso8601.UTC)


  def testParseDateTz(self):
    """Tests parse date tz."""
    d = iso8601.parseDate("2006-10-20T15:34:56.123+02:30")
    self.assertEquals(d.year, 2006)
    self.assertEquals(d.month, 10)
    self.assertEquals(d.day, 20)
    self.assertEquals(d.hour, 15)
    self.assertEquals(d.minute, 34)
    self.assertEquals(d.second, 56)
    self.assertEquals(d.microsecond, 123000)
    self.assertEquals(d.tzinfo.tzname(None), "+02:30")
    offset = d.tzinfo.utcoffset(None)
    self.assertEquals(offset.days, 0)
    self.assertEquals(offset.seconds, 60 * 60 * 2.5)


  def testParseDateTz2(self):
    """Tests parse date tz."""
    d = iso8601.parseDate("2006-10-20T15:34:56.123+0230")
    self.assertEquals(d.year, 2006)
    self.assertEquals(d.month, 10)
    self.assertEquals(d.day, 20)
    self.assertEquals(d.hour, 15)
    self.assertEquals(d.minute, 34)
    self.assertEquals(d.second, 56)
    self.assertEquals(d.microsecond, 123000)
    self.assertEquals(d.tzinfo.tzname(None), "+0230")
    offset = d.tzinfo.utcoffset(None)
    self.assertEquals(offset.days, 0)
    self.assertEquals(offset.seconds, 60 * 60 * 2.5)

  def testParseDateTz3(self):
    """Tests parse date tz."""
    d = iso8601.parseDate("2006-10-20T15:34:56.123+02")
    self.assertEquals(d.year, 2006)
    self.assertEquals(d.month, 10)
    self.assertEquals(d.day, 20)
    self.assertEquals(d.hour, 15)
    self.assertEquals(d.minute, 34)
    self.assertEquals(d.second, 56)
    self.assertEquals(d.microsecond, 123000)
    self.assertEquals(d.tzinfo.tzname(None), "+02")
    offset = d.tzinfo.utcoffset(None)
    self.assertEquals(offset.days, 0)
    self.assertEquals(offset.seconds, 60 * 60 * 2)

  def testParseDateTz4(self):
    """Tets parse date tz."""
    d = iso8601.parseDate("2012-08-08T01:30:00+0530")
    self.assertEquals(d.year, 2012)
    self.assertEquals(d.month, 8)
    self.assertEquals(d.day, 8)
    self.assertEquals(d.hour, 1)
    self.assertEquals(d.minute, 30)
    self.assertEquals(d.second, 0)
    self.assertEquals(d.microsecond, 0)
    self.assertEquals(d.tzinfo.tzname(None), "+0530")
    offset = d.tzinfo.utcoffset(None)
    self.assertEquals(offset.days, 0)
    self.assertEquals(offset.seconds, 60 * 60 * 5.5)



  def testParseInvalidDate(self):
    """Tests parse invalid date."""
    try:
      iso8601.parseDate(None)
    except iso8601.ParseError:
      pass
    else:
      self.assertEquals(1, 2)


  def testParseInvalidDate2(self):
    """Tests parse invalid date."""
    try:
      iso8601.parseDate("23")
    except iso8601.ParseError:
      pass
    else:
      self.assertEquals(1, 2)


  def testParseNoTimezone(self):
    """issue 4 - Handle datetime string without timezone

    This tests what happens when you parse a date with no timezone. While not
    strictly correct this is quite common. I'll assume UTC for the time zone
    in this case.
    """
    d = iso8601.parseDate("2007-01-01T08:00:00")
    self.assertEquals(d.year, 2007)
    self.assertEquals(d.month, 1)
    self.assertEquals(d.day, 1)
    self.assertEquals(d.hour, 8)
    self.assertEquals(d.minute, 0)
    self.assertEquals(d.second, 0)
    self.assertEquals(d.microsecond, 0)
    self.assertEquals(d.tzinfo, iso8601.UTC)


  def testParseNoTimezoneDifferentDefault(self):
    """Tests parse no timezone different default."""
    tz = iso8601.FixedOffset(2, 0, "test offset")
    d = iso8601.parseDate("2007-01-01T08:00:00", default_timezone=tz)
    self.assertEquals(d.tzinfo, tz)


  def testSpaceSeparator(self):
    """Handle a separator other than T"""
    d = iso8601.parseDate("2007-06-23 06:40:34.00Z")
    self.assertEquals(d.year, 2007)
    self.assertEquals(d.month, 6)
    self.assertEquals(d.day, 23)
    self.assertEquals(d.hour, 6)
    self.assertEquals(d.minute, 40)
    self.assertEquals(d.second, 34)
    self.assertEquals(d.microsecond, 0)
    self.assertEquals(d.tzinfo, iso8601.UTC)


  def testUtcOffsets1(self):
    """Tests other UTC offset formats."""
    d = iso8601.parseDate("2012-09-08T20:00:00-0700")
    offset = d.tzinfo.utcoffset(None)
    self.assertEquals(offset.days, -1)
    self.assertEquals(offset.seconds, 24 * 60 * 60 - 60 * 60 * 7)


  def testUtcOffsets2(self):
    """Tests other UTC offset formats."""
    d = iso8601.parseDate("2012-09-08T20:00:00-07:00")
    offset = d.tzinfo.utcoffset(None)
    self.assertEquals(offset.days, -1)
    self.assertEquals(offset.seconds, 24 * 60 * 60 - 60 * 60 * 7)


  def testTimezoneless(self):
    """Tests the timezoneless event feature."""
    self.assertEquals(iso8601.isTimezoneLessEvent('2012-07-04T19:00:00-0700'), False)
    self.assertEquals(iso8601.isTimezoneLessEvent('2012-07-04T19:00:00'), True)


  def testParseDateLongYear(self):
    """Tests parsing of date for years with more than 4 digits."""
    d = iso8601.parseDate("42557-01-27T08:00:00")
    self.assertEquals(d.year, 9999)
