"""aiocaldav unittests. Test Journals."""
import uuid

import pytest
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import Calendar

from .fixtures import (backend, journal1)


@pytest.mark.asyncio
async def test_create_journal_1(backend, journal1):
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

    await cal.add_journal(journal1)

    journals = await cal.journals()
    assert len(journals) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0


@pytest.mark.asyncio
async def test_create_journal_2(backend, journal1):
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

    await cal.add_journal(journal1)

    journals = await cal.journals()
    assert len(journals) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0


@pytest.mark.asyncio
async def test_create_delete_calendar_with_journal(backend, journal1):
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

    await cal.add_journal(journal1)

    journals = await cal.journals()
    assert len(journals) == 1

    await cal.delete()

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    with pytest.raises(error.NotFoundError):
        await cal2.journals()


@pytest.mark.asyncio
async def test_create_journal_from_vobject(backend, journal1):
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
    vjournal1 = vobject.readOne(journal1)
    await cal.add_journal(vjournal1)

    journals = await cal.journals()
    assert len(journals) == 1

    events = await cal.events()
    assert len(events) == 0
    todos = await cal.todos()
    assert len(todos) == 0


@pytest.mark.asyncio
async def test_create_journal_in_event_only_calendar(backend, journal1):
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
        await cal.add_journal(journal1)
    else:
        with pytest.raises(error.PutError):
            await cal.add_journal(journal1)
