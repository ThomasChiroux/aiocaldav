"""aiocaldav unittests. Test Availability."""
import uuid

import pytest
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import Calendar, Availability

from .fixtures import (backend, caldav, principal, availability_fixtures,
                       avail1, avail2)


@pytest.mark.asyncio
async def test_create_availability_1(backend, principal, availability_fixtures):
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(availability_fixtures)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0
    journals = await cal.journals()
    assert len(journals) == 0


@pytest.mark.asyncio
async def test_create_availability_2(backend, principal, availability_fixtures):
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(
        name="Yep", cal_id=cal_id,
        supported_calendar_component_set=['VAVAILABILITY'])

    await cal.add_availability(availability_fixtures)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0
    journals = await cal.journals()
    assert len(journals) == 0

@pytest.mark.asyncio
async def test_create_2_availability(backend, principal, 
                                     avail1, avail2):
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail1)
    await cal.add_availability(avail2)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 2

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0
    journals = await cal.journals()
    assert len(journals) == 0




@pytest.mark.asyncio
async def test_create_delete_calendar_with_avail(backend, caldav, principal, 
                                                 availability_fixtures):
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)
    assert cal_id in str(cal.url.canonical())
    events = await cal.events()
    assert len(events) == 0

    await cal.add_availability(availability_fixtures)

    avails = await cal.availabilities()
    assert len(avails) == 1

    await cal.delete()

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    with pytest.raises(error.NotFoundError):
        await cal2.availabilities()


@pytest.mark.asyncio
async def test_create_avail_from_vobject(backend, caldav, principal, 
                                         availability_fixtures):
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    # add event from vobject data
    vavailability_fixtures = vobject.readOne(availability_fixtures)
    await cal.add_availability(vavailability_fixtures)

    avails = await cal.availabilities()
    assert len(avails) == 1

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    avails2 = await cal2.availabilities()
    assert len(avails2) == 1
    assert avails2[0].url == avails[0].url


@pytest.mark.asyncio
async def test_lookup_avail_1(backend, caldav, principal, availability_fixtures):
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)
    assert cal_id in str(cal.url.canonical())
    avails = await cal.availabilities()
    assert len(avails) == 0

    av1 = await cal.add_availability(availability_fixtures)
    assert av1.url is not None

    av2 = await cal.availability_by_url(av1.url)
    av3 = await cal.availability_by_uid(av1.instance.vavailability.uid.valueRepr())
    assert av2.instance.vavailability.uid == av1.instance.vavailability.uid
    assert av3.instance.vavailability.uid == av1.instance.vavailability.uid
    # Knowing the URL of an event, we should be able to get to it
    # without going through a calendar object
    av4 = Availability(client=caldav, url=av1.url)
    await av4.load()
    assert av4.instance.vavailability.uid == av1.instance.vavailability.uid

    with pytest.raises(error.NotFoundError):
        await cal.availability_by_uid("0")


@pytest.mark.asyncio
async def test_delete_availability_1(backend, principal, availability_fixtures):
    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)
    assert cal_id in str(cal.url.canonical())
    avails = await cal.availabilities()
    assert len(avails) == 0

    av1 = await cal.add_availability(availability_fixtures)
    assert av1.url is not None

    await av1.delete()

    with pytest.raises(error.NotFoundError):
        await cal.availability_by_url(av1.url)

    with pytest.raises(error.NotFoundError):
        await cal.availability_by_uid(av1.instance.vavailability.uid.valueRepr())
