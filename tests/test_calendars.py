"""aiocaldav unittests. Test Principal and Calendars."""
import uuid

import pytest

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import CalendarSet

from .fixtures import backend, caldav, principal


@pytest.mark.asyncio
async def test_principal_default(backend, principal):
    uri = backend.get('uri')
    login = backend.get('login', uuid.uuid4().hex)
    assert principal.url == uri + login + "/"
    assert principal._calendar_home_set is None


@pytest.mark.asyncio
async def test_calendars_default(principal):
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)


@pytest.mark.asyncio
async def test_calendars_local(principal):
    """Create a local calendar without creating it on the server."""
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)
    cal_id = uuid.uuid4().hex

    cal = await principal.calendar(name="Yep", cal_id=cal_id)
    assert cal.url is not None
    assert cal_id in str(cal.url.canonical())


@pytest.mark.asyncio
async def test_create_calendars(principal):
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)
    assert cal.url is not None
    assert cal_id in str(cal.url.canonical())
    events = await cal.events()
    assert len(events) == 0
    events2 = await (await principal.calendar(name="Yep", cal_id=cal_id)).events()
    assert len(events2) == 0


@pytest.mark.asyncio
async def test_create_calendars_component_set(principal):
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VEVENT'])
    assert cal.url is not None
    assert cal_id in str(cal.url.canonical())
    events = await cal.events()
    assert len(events) == 0
    events2 = await (await principal.calendar(name="Yep", cal_id=cal_id)).events()
    assert len(events2) == 0


@pytest.mark.asyncio
async def test_create_delete_calendars(principal):
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)
    assert cal_id in str(cal.url.canonical())
    events = await cal.events()
    assert len(events) == 0
    cal2 = await principal.calendar(name="Yep", cal_id=cal_id)
    assert cal_id in str(cal2.url.canonical())

    await cal.delete()

    cal3 = await principal.calendar(name="Yep", cal_id=cal_id)
    assert cal3.url is not None
    assert cal_id in str(cal3.url.canonical())
    with pytest.raises(error.NotFoundError):
        await cal3.events()
