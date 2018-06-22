"""
Principal.calendar() and CalendarSet.calendar() should create
Calendar objects without initiating any communication with the
server.  Calendar.event() should create Event object without
initiating any communication with the server.

DAVClient.__init__ also doesn't do any communication
Principal.__init__ as well, if the principal_url is given
Principal.calendar_home_set needs to be set or the server will be queried
"""

import pytest

from aiocaldav.davclient import DAVClient
from aiocaldav.objects import (Principal, CalendarSet, Calendar)


@pytest.mark.asyncio
async def test_calendar_1():
    cal_url = "http://me:hunter2@calendar.example:80/"
    client = DAVClient(url=cal_url)

    principal = Principal(client, cal_url + "me/")
    principal._calendar_home_setter(cal_url + "me/calendars/")

    # calendar_home_set is actually a CalendarSet object
    assert isinstance(await principal.calendar_home_set(), CalendarSet)

    calendar1 = await principal.calendar(name="foo", cal_id="bar")
    calendar2 = (await principal.calendar_home_set()).calendar(
        name="foo", cal_id="bar")
    assert calendar1.url == calendar2.url
    assert calendar1.url == "http://calendar.example:80/me/calendars/bar/"

    # principal.calendar_home_set can also be set to an object
    # This should be noop
    principal._calendar_home_setter(await principal.calendar_home_set())
    calendar1 = await principal.calendar(name="foo", cal_id="bar")

    assert calendar1.url == calendar2.url


def test_calendar_2():
    cal_url = "http://me:hunter2@calendar.example:80/"
    client = DAVClient(url=cal_url)

    # When building a calendar from a relative URL and a client,
    # the relative URL should be appended to the base URL in the client
    calendar1 = Calendar(client, 'someoneelse/calendars/main_calendar')
    calendar2 = Calendar(client,
                         'http://me:hunter2@calendar.example:80/someoneelse/calendars/main_calendar')
    assert calendar1.url == calendar2.url


def test_default_client():
    """When no client is given to a DAVObject, but the parent is given,
    parent.client will be used"""
    cal_url = "http://me:hunter2@calendar.example:80/"
    client = DAVClient(url=cal_url)
    calhome = CalendarSet(client, cal_url + "me/")
    calendar = Calendar(parent=calhome)
    assert calendar.client == calhome.client
