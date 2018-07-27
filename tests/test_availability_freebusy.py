"""aiocaldav unittests. Test Freebusy with Availability."""
import datetime
import uuid

from dateutil.tz import tzutc
import pytest
import pytz
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import Calendar, Availability, FreeBusy

from .fixtures import (backend, caldav, principal, availability_fixtures,
                       avail4fb, avail4fb2_prio5, event4avail)


@pytest.mark.asyncio
async def test_create_availability_freebusy_1(backend, principal, avail4fb):
    """test freebusy with avail: no freebusy period."""
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail4fb)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 1

    freebusy = await cal.freebusy_request(datetime.datetime(2018, 7, 30, 8, 0, 0),
                                          datetime.datetime(2018, 7, 30, 16, 0, 0))

    assert isinstance(freebusy, FreeBusy)
    assert freebusy.instance.vfreebusy
    with pytest.raises(AttributeError):
        assert len(freebusy.instance.vfreebusy_freebusy_list) == 0


@pytest.mark.asyncio
async def test_create_availability_freebusy_2(backend, principal, avail4fb):
    """test freebusy with avail: 1 freebusy period."""
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail4fb)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 1

    freebusy = await cal.freebusy_request(datetime.datetime(2018, 7, 30, 10, 0, 0),
                                          datetime.datetime(2018, 7, 30, 23, 59, 59))

    assert isinstance(freebusy, FreeBusy)
    assert len(freebusy.instance.vfreebusy.freebusy_list) == 1

    assert freebusy.instance.vfreebusy.freebusy_list[0].value[0] == (
        datetime.datetime(2018, 7, 30, 17, 0, tzinfo=pytz.utc),
        datetime.datetime(2018, 7, 30, 23, 59, 59, tzinfo=pytz.utc))


@pytest.mark.asyncio
async def test_create_availability_freebusy_3(backend, principal, avail4fb):
    """test freebusy with avail: 3 freebusy period."""
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail4fb)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 1

    freebusy = await cal.freebusy_request(datetime.datetime(2018, 7, 30, 10, 0, 0),
                                          datetime.datetime(2018, 7, 31, 22, 00, 00))

    assert isinstance(freebusy, FreeBusy)
    assert len(freebusy.instance.vfreebusy.freebusy_list) == 2

    assert freebusy.instance.vfreebusy.freebusy_list[0].value[0] == (
        datetime.datetime(2018, 7, 30, 17, 0, tzinfo=pytz.utc),
        datetime.datetime(2018, 7, 31, 9, 0, tzinfo=pytz.utc))

    assert freebusy.instance.vfreebusy.freebusy_list[1].value[0] == (
        datetime.datetime(2018, 7, 31, 17, 0, tzinfo=pytz.utc),
        datetime.datetime(2018, 7, 31, 22, 0, tzinfo=pytz.utc))


@pytest.mark.asyncio
async def test_create_availability_freebusy_vacations_1(backend, principal, 
                                                        avail4fb, avail4fb2_prio5):
    """test freebusy with avail: no freebusy period."""
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail4fb)
    await cal.add_availability(avail4fb2_prio5)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 2

    freebusy = await cal.freebusy_request(datetime.datetime(2018, 7, 30, 10, 0, 0),
                                          datetime.datetime(2018, 7, 30, 23, 59, 59))

    assert isinstance(freebusy, FreeBusy)
    assert freebusy.instance.vfreebusy
    with pytest.raises(AttributeError):
        assert len(freebusy.instance.vfreebusy_freebusy_list) == 0


@pytest.mark.asyncio
async def test_create_availability_freebusy_vacations_2(backend, principal, 
                                                        avail4fb, avail4fb2_prio5):
    """test freebusy with avail: test at the end of the vacations."""
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail4fb)
    await cal.add_availability(avail4fb2_prio5)

    availabilities = await cal.availabilities()
    assert len(availabilities) == 2

    freebusy = await cal.freebusy_request(datetime.datetime(2018, 8, 16, 10, 0, 0),
                                          datetime.datetime(2018, 8, 17, 15, 0, 0))

    assert isinstance(freebusy, FreeBusy)
    assert len(freebusy.instance.vfreebusy.freebusy_list) == 1

    assert freebusy.instance.vfreebusy.freebusy_list[0].value[0] == (
        datetime.datetime(2018, 8, 16, 10, 0, tzinfo=pytz.utc),
        datetime.datetime(2018, 8, 17, 9, 0, tzinfo=pytz.utc))


@pytest.mark.asyncio
async def test_create_availability_freebusy_with_event(backend, principal, 
                                                       avail4fb, event4avail):
    """test freebusy with avail: no freebusy period."""
    if backend.get("name") not in ["cyrus", ]:
        # only cyrus support vailability for now
        pytest.skip()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_availability(avail4fb)
    await cal.add_event(event4avail)

    
    freebusy = await cal.freebusy_request(datetime.datetime(2018, 7, 30, 10, 0, 0),
                                          datetime.datetime(2018, 7, 30, 23, 59, 59))

    assert isinstance(freebusy, FreeBusy)
    assert len(freebusy.instance.vfreebusy.freebusy_list) == 2

    assert freebusy.instance.vfreebusy.freebusy_list[0].value[0] == (
        datetime.datetime(2018, 7, 30, 12, 0, tzinfo=pytz.utc),
        datetime.datetime(2018, 7, 30, 13, 30, tzinfo=pytz.utc))

    assert freebusy.instance.vfreebusy.freebusy_list[1].value[0] == (
        datetime.datetime(2018, 7, 30, 17, 0, tzinfo=pytz.utc),
        datetime.datetime(2018, 7, 30, 23, 59, 59, tzinfo=pytz.utc))