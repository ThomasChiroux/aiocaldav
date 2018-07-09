"""aiocaldav unittests. Test Principal and Calendars."""
import uuid

import pytest

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import CalendarSet

from .fixtures import backend


@pytest.mark.asyncio
async def test_principal_default(backend):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
    assert principal.url == uri + login + "/"
    assert principal._calendar_home_set is None

    await principal.prune()


@pytest.mark.asyncio
async def test_calendars_default(backend):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)

    await principal.prune()


@pytest.mark.asyncio
async def test_calendars_local(backend):
    """Create a local calendar without creating it on the server."""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)
    cal_id = uuid.uuid4().hex

    cal = await principal.calendar(name="Yep", cal_id=cal_id)
    assert cal.url is not None
    assert cal_id in str(cal.url.canonical())

    await principal.prune()


@pytest.mark.asyncio
async def test_create_calendars(backend):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
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

    await principal.prune()


@pytest.mark.asyncio
async def test_create_calendars_component_set(backend):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
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

    await principal.prune()


@pytest.mark.asyncio
async def test_create_delete_calendars(backend):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

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

    await principal.prune()
