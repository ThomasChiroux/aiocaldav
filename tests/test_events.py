"""aiocaldav unittests. Test Events."""
import datetime
import uuid

import pytest
import pytz
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import (Calendar, Event, FreeBusy)

from .fixtures import (backend, event_fixtures, event1, event2, event3)


@pytest.mark.asyncio
async def test_create_event_1(backend, event_fixtures):
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

    await cal.add_event(event_fixtures)

    # c.events() should give a full list of events
    events = await cal.events()
    assert len(events) == 1

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    events2 = await cal2.events()
    assert len(events2) == 1
    assert events2[0].url == events[0].url

    await principal.prune()


@pytest.mark.asyncio
async def test_create_event_2(backend, event_fixtures):
    """test with a VEVENT only calendar."""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VEVENT'])
    assert cal_id in str(cal.url.canonical())
    events = await cal.events()
    assert len(events) == 0

    await cal.add_event(event_fixtures)

    # c.events() should give a full list of events
    events = await cal.events()
    assert len(events) == 1

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    events2 = await cal2.events()
    assert len(events2) == 1
    assert events2[0].url == events[0].url

    await principal.prune()


@pytest.mark.asyncio
async def test_create_2events(backend, event1, event2):
    """test with a VEVENT only calendar."""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VEVENT'])
    assert cal_id in str(cal.url.canonical())
    events = await cal.events()
    assert len(events) == 0

    await cal.add_event(event1)
    await cal.add_event(event2)

    # c.events() should give a full list of events
    events = await cal.events()
    assert len(events) == 2

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    events2 = await cal2.events()
    assert len(events2) == 2
    assert events2[0].url == events[0].url
    assert events2[1].url == events[1].url

    await principal.prune()


@pytest.mark.asyncio
async def test_create_delete_calendar_with_event(backend, event_fixtures):
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

    await cal.add_event(event_fixtures)

    # c.events() should give a full list of events
    events = await cal.events()
    assert len(events) == 1

    await cal.delete()

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    with pytest.raises(error.NotFoundError):
        await cal2.events()

    await principal.prune()


@pytest.mark.asyncio
async def test_create_event_from_vobject(backend, event_fixtures):
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

    # add event from vobject data
    vevent_fixtures = vobject.readOne(event_fixtures)
    await cal.add_event(vevent_fixtures)

    # c.events() should give a full list of events
    events = await cal.events()
    assert len(events) == 1

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    events2 = await cal2.events()
    assert len(events2) == 1
    assert events2[0].url == events[0].url

    await principal.prune()


@pytest.mark.asyncio
async def test_lookup_event_1(backend, event_fixtures):
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

    ev1 = await cal.add_event(event_fixtures)
    assert ev1.url is not None

    ev2 = await cal.event_by_url(ev1.url)
    ev3 = await cal.event_by_uid(ev1.instance.vevent.uid.valueRepr())
    assert ev2.instance.vevent.uid == ev1.instance.vevent.uid
    assert ev3.instance.vevent.uid == ev1.instance.vevent.uid
    # Knowing the URL of an event, we should be able to get to it
    # without going through a calendar object
    ev4 = Event(client=caldav, url=ev1.url)
    await ev4.load()
    assert ev4.instance.vevent.uid == ev1.instance.vevent.uid

    with pytest.raises(error.NotFoundError):
        await cal.event_by_uid("0")

    await principal.prune()


@pytest.mark.asyncio
async def test_delete_event_1(backend, event_fixtures):
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

    ev1 = await cal.add_event(event_fixtures)
    assert ev1.url is not None

    await ev1.delete()

    with pytest.raises(error.NotFoundError):
        await cal.event_by_url(ev1.url)

    with pytest.raises(error.NotFoundError):
        await cal.event_by_uid(ev1.instance.vevent.uid.valueRepr())

    await principal.prune()


@pytest.mark.asyncio
async def test_create_event_in_journal_only_calendar(backend, event_fixtures):
    """This test does not pass with radicale backend: perhaps radicale accepts
    events even when the calendar should not support it ?"""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VJOURNAL'])
    if backend.get("name") in ["radicale", "davical", "xandikos"]:
        await cal.add_event(event_fixtures)
    else:
        with pytest.raises(error.PutError):
            await cal.add_event(event_fixtures)

    await principal.prune()


@pytest.mark.asyncio
async def test_create_event_in_todo_only_calendar(backend, event_fixtures):
    """This test does not pass with radicale backend: perhaps radicale accepts
    events even when the calendar should not support it ?"""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VTODO'])
    if backend.get("name") in ["radicale", "davical", "xandikos"]:
        await cal.add_event(event_fixtures)
    else:
        with pytest.raises(error.PutError):
            await cal.add_event(event_fixtures)

    await principal.prune()


@pytest.mark.asyncio
async def test_date_search_naive_1(backend, event1, event2):
    """Test naive date search."""
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

    evt1 = await cal.add_event(event1)

    result = await cal.date_search(datetime.datetime(2006, 7, 13, 17, 00, 00),
                                   datetime.datetime(2006, 7, 15, 17, 00, 00))
    assert len(result) == 1
    assert evt1.instance.vevent.uid == result[0].instance.vevent.uid

    # event2 is same UID, but one year ahead.
    # The timestamp should change.
    evt1.data = event2
    await evt1.save()

    result2 = await cal.date_search(datetime.datetime(2006, 7, 13, 17, 00, 00),
                                    datetime.datetime(2006, 7, 15, 17, 00, 00))
    assert len(result2) == 0

    result3 = await cal.date_search(datetime.datetime(2007, 7, 13, 17, 00, 00),
                                    datetime.datetime(2007, 7, 15, 17, 00, 00))
    assert len(result3) == 1

    # date search without closing date should also find it
    result4 = await cal.date_search(datetime.datetime(2007, 7, 13, 17, 00, 00))
    assert len(result4) == 1

    await principal.prune()


@pytest.mark.asyncio
async def test_date_search_tzaware_gmt_1(backend, event1, event2):
    """Test naive date search."""
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

    evt1 = await cal.add_event(event1)

    result = await cal.date_search(datetime.datetime(2006, 7, 13, 17, 00, 00,
                                                     tzinfo=datetime.timezone.utc),
                                   datetime.datetime(2006, 7, 15, 17, 00, 00,
                                                     tzinfo=datetime.timezone.utc))

    assert len(result) == 1
    assert evt1.instance.vevent.uid == result[0].instance.vevent.uid

    # event2 is same UID, but one year ahead.
    # The timestamp should change.
    evt1.data = event2
    await evt1.save()

    result2 = await cal.date_search(datetime.datetime(2006, 7, 13, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc),
                                    datetime.datetime(2006, 7, 15, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc))
    assert len(result2) == 0

    result3 = await cal.date_search(datetime.datetime(2007, 7, 13, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc),
                                    datetime.datetime(2007, 7, 15, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc))
    assert len(result3) == 1

    # date search without closing date should also find it
    result4 = await cal.date_search(datetime.datetime(2007, 7, 13, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc))
    assert len(result4) == 1

    await principal.prune()


@pytest.mark.asyncio
async def test_date_search_tzaware_2(backend, event1):
    """Test naive date search."""
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

    evt1 = await cal.add_event(event1)

    start = datetime.datetime(2006, 7, 14, 16, 00, 00,
                              tzinfo=datetime.timezone.utc)
    start = pytz.timezone(
        "Europe/Paris").normalize(start.astimezone(pytz.timezone('Europe/Paris')))

    end = datetime.datetime(2006, 7, 14, 18, 00, 00,
                            tzinfo=datetime.timezone.utc)
    end = pytz.timezone(
        "Europe/Paris").normalize(end.astimezone(pytz.timezone('Europe/Paris')))
    result = await cal.date_search(start, end)

    assert len(result) == 1
    assert evt1.instance.vevent.uid == result[0].instance.vevent.uid

    start = datetime.datetime(2006, 7, 14, 18, 00, 00,
                              tzinfo=datetime.timezone.utc)
    start = pytz.timezone(
        "Europe/Paris").normalize(start.astimezone(pytz.timezone('Europe/Paris')))

    end = datetime.datetime(2006, 7, 14, 19, 00, 00,
                            tzinfo=datetime.timezone.utc)
    end = pytz.timezone(
        "Europe/Paris").normalize(end.astimezone(pytz.timezone('Europe/Paris')))
    result = await cal.date_search(start, end)

    assert len(result) == 1
    # assert evt1.instance.vevent.uid == result[0].instance.vevent.uid

    await principal.prune()


@pytest.mark.asyncio
async def test_recurring_date_search(backend, event3):
    """
    This is more sanity testing of the server side than testing of the
    library per se.  How will it behave if we serve it a recurring
    event?
    """

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

    evt = await cal.add_event(event3)

    result = await cal.date_search(datetime.datetime(2008, 11, 1, 17, 00, 00,
                                                     tzinfo=datetime.timezone.utc),
                                   datetime.datetime(2008, 11, 3, 17, 00, 00,
                                                     tzinfo=datetime.timezone.utc))

    assert len(result) == 1
    assert result[0].data.count("END:VEVENT") == 1

    result2 = await cal.date_search(datetime.datetime(2008, 11, 1, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc),
                                    datetime.datetime(2008, 11, 3, 17, 00, 00,
                                                      tzinfo=datetime.timezone.utc))
    assert len(result2) == 1

    # So much for standards ... seems like different servers
    # behaves differently
    # COMPATIBILITY PROBLEMS - look into it
    # if "RRULE" in result2[0].data and "BEGIN:STANDARD" not in result2[0].data:
    assert result2[0].data.count("END:VEVENT") == 1
    # else:
    #    assert result2[0].data.count("END:VEVENT") == 2

    # The recurring events should not be expanded when using the
    # events() method
    events = await cal.events()
    assert len(events) == 1
