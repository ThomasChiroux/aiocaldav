"""aiocaldav unittests. Test Journals."""
import uuid

import pytest
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import Calendar, Journal

from .fixtures import (backend, journal_fixtures)


@pytest.mark.asyncio
async def test_create_journal_1(backend, journal_fixtures):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    await cal.add_journal(journal_fixtures)

    journals = await cal.journals()
    assert len(journals) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0


@pytest.mark.asyncio
async def test_create_journal_2(backend, journal_fixtures):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VJOURNAL'])

    await cal.add_journal(journal_fixtures)

    journals = await cal.journals()
    assert len(journals) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0


@pytest.mark.asyncio
async def test_create_delete_calendar_with_journal(backend, journal_fixtures):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VJOURNAL'])

    await cal.add_journal(journal_fixtures)

    journals = await cal.journals()
    assert len(journals) == 1

    await cal.delete()

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    with pytest.raises(error.NotFoundError):
        await cal2.journals()


@pytest.mark.asyncio
async def test_create_journal_from_vobject(backend, journal_fixtures):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    # add event from vobject data
    vjournal_fixtures = vobject.readOne(journal_fixtures)
    await cal.add_journal(vjournal_fixtures)

    journals = await cal.journals()
    assert len(journals) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0


@pytest.mark.asyncio
async def test_lookup_journal_1(backend, journal_fixtures):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    jnl1 = await cal.add_journal(journal_fixtures)
    assert jnl1.url is not None

    jnl2 = await cal.journal_by_url(jnl1.url)
    jnl3 = await cal.journal_by_uid(jnl1.instance.vjournal.uid.valueRepr())
    assert jnl2.instance.vjournal.uid == jnl1.instance.vjournal.uid
    assert jnl3.instance.vjournal.uid == jnl1.instance.vjournal.uid
    # Knowing the URL of an event, we should be able to get to it
    # without going through a calendar object
    jnl4 = Journal(client=caldav, url=jnl1.url)
    await jnl4.load()
    assert jnl4.instance.vjournal.uid == jnl1.instance.vjournal.uid

    with pytest.raises(error.NotFoundError):
        await cal.journal_by_uid("0")


@pytest.mark.asyncio
async def test_delete_journal_1(backend, journal_fixtures):
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id)

    jnl1 = await cal.add_journal(journal_fixtures)
    assert jnl1.url is not None

    await jnl1.delete()

    with pytest.raises(error.NotFoundError):
        await cal.journal_by_url(jnl1.url)

    with pytest.raises(error.NotFoundError):
        await cal.journal_by_uid(jnl1.instance.vjournal.uid.valueRepr())


@pytest.mark.asyncio
async def test_create_journal_in_event_only_calendar(backend, journal_fixtures):
    """This test does not pass with radicale backend: perhaps radicale accepts
    journal even when the calendar should not support it ?"""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = uuid.uuid4().hex
    password = uuid.uuid4().hex
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    cal_id = uuid.uuid4().hex
    cal = await principal.make_calendar(name="Yep", cal_id=cal_id,
                                        supported_calendar_component_set=['VEVENT'])
    if backend.get("name") == "radicale":
        await cal.add_journal(journal_fixtures)
    else:
        with pytest.raises(error.PutError):
            await cal.add_journal(journal_fixtures)
