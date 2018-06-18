"""aiocaldav unittests. Test Principal."""
import contextlib
import subprocess
import time

import pytest

from .conf import backends

from caldav.davclient import DAVClient
from caldav.objects import CalendarSet


@contextlib.contextmanager
def caldav_server():
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml up -d".format(
            location=backends.get('radicale', {}).get("location")),
        shell=True)
    time.sleep(5)  # wait for the container to starts
    yield backends.get('radicale', {})
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml down".format(
            location=backends.get('radicale', {}).get("location")),
        shell=True)
    time.sleep(3)  # wait for the container to stop


@pytest.fixture(scope="module")
def backend(request):
    with caldav_server() as backend:
        yield backend


@pytest.mark.asyncio
async def test_empty_ok(backend):
    assert True


@pytest.mark.asyncio
async def test_principal_default(backend):
    uri = backend.get('uri')
    login = backend.get('login')
    password = backend.get('password')
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
    assert principal.url == uri + 'toto/'
    assert principal._calendar_home_set is None


@pytest.mark.asyncio
async def test_calendars_default(backend):
    uri = backend.get('uri')
    login = backend.get('login')
    password = backend.get('password')
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()
    collections = await principal.calendars()
    assert len(collections) == 0
    assert isinstance(principal._calendar_home_set, CalendarSet)
