"""aiocaldav unittests. Test Todos."""
import uuid

import pytest
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import Calendar

from .fixtures import (backend, todo1)


@pytest.mark.asyncio
async def test_create_todo_with_completed_1(backend, todo1):
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

    await cal.add_todo(todo1)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0


@pytest.mark.asyncio
async def test_create_todo_with_completed_2(backend, todo1):
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
                                        supported_calendar_component_set=['VTODO'])

    await cal.add_todo(todo1)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0


@pytest.mark.asyncio
async def test_create_todo_without_completed_1(backend, todo1):
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

    await cal.add_todo(todo1)

    todos = await cal.todos()
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0


@pytest.mark.asyncio
async def test_create_todo_without_completed_2(backend, todo1):
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
                                        supported_calendar_component_set=['VTODO'])

    await cal.add_todo(todo1)

    todos = await cal.todos()
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0


@pytest.mark.asyncio
async def test_create_delete_calendar_with_todo(backend, todo1):
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
                                        supported_calendar_component_set=['VTODO'])

    await cal.add_todo(todo1)

    todos = await cal.todos()
    assert len(todos) == 1

    await cal.delete()

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    with pytest.raises(error.NotFoundError):
        await cal2.todos()


@pytest.mark.asyncio
async def test_create_todo_from_vobject(backend, todo1):
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
    vtodo1 = vobject.readOne(todo1)
    await cal.add_todo(vtodo1)

    todos = await cal.todos()
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0


@pytest.mark.asyncio
async def test_create_todo_mark_completed_1(backend, todo1):
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

    todo = await cal.add_todo(todo1)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    await todo.complete()

    todos2 = await cal.todos(include_completed=True)
    assert len(todos2) == 1

    todos3 = await cal.todos(include_completed=False)
    assert len(todos3) == 0


@pytest.mark.asyncio
async def test_create_todo_in_event_only_calendar(backend, todo1):
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
        await cal.add_todo(todo1)
    else:
        with pytest.raises(error.PutError):
            await cal.add_todo(todo1)
