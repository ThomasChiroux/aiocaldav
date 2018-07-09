"""aiocaldav unittests. Test Todos."""
import uuid

import pytest
import vobject

from aiocaldav.davclient import DAVClient
from aiocaldav.lib import error
from aiocaldav.objects import Calendar

from .fixtures import (backend, todo_fixtures)


@pytest.mark.asyncio
async def test_create_todo_with_completed_1(backend, todo_fixtures):
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

    await cal.add_todo(todo_fixtures)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_with_completed_2(backend, todo_fixtures):
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

    await cal.add_todo(todo_fixtures)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_without_completed_1(backend, todo_fixtures):
    vtodo = vobject.readOne(todo_fixtures)
    try:
        _ = vtodo.vtodo.status
    except AttributeError:  # no status
        if backend.get("name") == "radicale":
            # Radicale needs a status in todo
            pytest.skip()

    try:
        _ = vtodo.vtodo.completed
    except AttributeError:
        pass

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

    await cal.add_todo(todo_fixtures)

    todos = await cal.todos(include_completed=False)

    try:
        _ = vtodo.vtodo.completed
    except (AttributeError, KeyError):  # no completed, should be in the list
        assert len(todos) == 1
    else:
        assert len(todos) == 0

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_without_completed_2(backend, todo_fixtures):
    vtodo = vobject.readOne(todo_fixtures)
    try:
        _ = vtodo.vtodo.status
    except AttributeError:  # no status
        if backend.get("name") == "radicale":
            pytest.skip()

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

    await cal.add_todo(todo_fixtures)

    todos = await cal.todos(include_completed=False)
    try:
        _ = vtodo.vtodo.completed
    except (AttributeError, KeyError):  # no completed, should be in the list
        assert len(todos) == 1
    else:
        assert len(todos) == 0

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_delete_calendar_with_todo(backend, todo_fixtures):
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

    await cal.add_todo(todo_fixtures)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    await cal.delete()

    # We should be able to access the calender through the URL
    cal2 = Calendar(client=caldav, url=cal.url)
    with pytest.raises(error.NotFoundError):
        await cal2.todos()

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_from_vobject_1(backend, todo_fixtures):
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
    vtodo_fixtures = vobject.readOne(todo_fixtures)
    await cal.add_todo(vtodo_fixtures)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_from_vobject_2(backend, todo_fixtures):
    vtodo = vobject.readOne(todo_fixtures)
    try:
        _ = vtodo.vtodo.status
    except AttributeError:  # no status
        if backend.get("name") == "radicale":
            pytest.skip()

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
    vtodo_fixtures = vobject.readOne(todo_fixtures)
    await cal.add_todo(vtodo_fixtures)

    todos = await cal.todos(include_completed=False)
    try:
        _ = vtodo.vtodo.completed
    except (AttributeError, KeyError):  # no completed, should be in the list
        assert len(todos) == 1
    else:
        assert len(todos) == 0

    events = await cal.events()
    assert len(events) == 0
    journals = await cal.journals()
    assert len(journals) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_mark_completed_1(backend, todo_fixtures):
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

    todo = await cal.add_todo(todo_fixtures)

    todos = await cal.todos(include_completed=True)
    assert len(todos) == 1

    await todo.complete()

    todos2 = await cal.todos(include_completed=True)
    assert len(todos2) == 1

    todos3 = await cal.todos(include_completed=False)
    assert len(todos3) == 0

    await principal.prune()


@pytest.mark.asyncio
async def test_create_todo_in_event_only_calendar(backend, todo_fixtures):
    """This test does not pass with radicale backend: perhaps radicale accepts
    journal even when the calendar should not support it ?"""
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
    if backend.get("name") in ["radicale", "davical", "xandikos"]:
        await cal.add_todo(todo_fixtures)
    else:
        with pytest.raises(error.PutError):
            await cal.add_todo(todo_fixtures)

    await principal.prune()
