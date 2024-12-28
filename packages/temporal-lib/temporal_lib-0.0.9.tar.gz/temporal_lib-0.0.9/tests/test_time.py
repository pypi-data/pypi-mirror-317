#!/bin/python

from datetime import datetime, time
from zoneinfo import ZoneInfo

from temporal_lib.tlib_types import timestr_to_time
from temporal_lib.core import localize_datetime
from temporal_lib.tlib_timezone import TimeZone

def test_string_to_time():

	time_string = "1AM"
	expected_time = time(1, 0, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "2PM"
	expected_time = time(14, 0, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "13"
	expected_time = time(13, 0, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "1:30AM"
	expected_time = time(1, 30, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "1:30PM"
	expected_time = time(13, 30, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "12:30PM"
	expected_time = time(12, 30, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "12:30PM"
	expected_time = time(12, 30, 0)
	assert timestr_to_time(time_string) == expected_time


def test_localize_datetime():

	naive_datetime = datetime(year=2001, month=1, day=1, hour=2, minute=3, second=4)
	tz_string = "America/Los_Angeles"
	tz_zoneinfo = ZoneInfo(tz_string)
	expected = datetime(year=2001, month=1, day=1, hour=2, minute=3, second=4, tzinfo=tz_zoneinfo)

	# Test One
	assert localize_datetime(naive_datetime, tz_string) == expected

	# Test Two
	actual = localize_datetime(naive_datetime, tz_zoneinfo)
	assert actual == expected

	# Test Three
	assert localize_datetime(naive_datetime, TimeZone(tz_string)) == expected
