"""Fixtures for tests."""
import contextlib
import glob
import os
import subprocess
import time
import uuid
import urllib.request
import urllib.error

import pytest

from aiocaldav.davclient import DAVClient
from .conf import backends


def get_one_static_file(filename, full_path=True):
    """Return content of a static file.

    :param str filename: either full file path and name or only file name
    :param bool full_path: if True filename is full path, if False, calculates the
                           path.
    """
    if not full_path:
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        filename = os.path.join(static_dir, filename)
    with open(filename, "r") as fd:
        content = fd.read()
    return content


def get_static_files_list(filetype="event", ok=True):
    """return a list of icalendar from static directory.

    :param str filetype: type of files in ['event', 'journal', 'todo']
    :param bool ok: if True return OK files (should not generate an error)
                    if False returns NOK files (should generate an error)
    """
    if ok:
        oktype = "ok"
    else:
        oktype = "nok"
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    searched_files = os.path.join(static_dir, f"{filetype}_{oktype}*.ics")
    return sorted(glob.glob(searched_files))


def check_docker():
    """Check if docker is running."""
    try:
        subprocess.run("docker ps", shell=True).check_returncode()
    except subprocess.CalledProcessError:
        raise Exception(
            "Docker seems not started. Start it before running tests")


@contextlib.contextmanager
def radicale_docker():
    check_docker()
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml up -d".format(
            location=backends.get('radicale', {}).get("location")),
        shell=True)
    # TODO: instead of waiting a fixed time, check if caldav server is started with
    #       a http get loop for example
    time.sleep(5)  # wait for the container to starts
    yield backends.get('radicale', {})
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml down".format(
            location=backends.get('radicale', {}).get("location")),
        shell=True)
    time.sleep(3)  # wait for the container to stop


@contextlib.contextmanager
def radicale_direct():
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    yield backends.get('radicale2', {})


@contextlib.contextmanager
def davical_docker():
    check_docker()
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml up -d".format(
            location=backends.get('davical', {}).get("location")),
        shell=True)
    time.sleep(5)  # wait for the container to starts
    # wait for the services to respond (davical responds 401 when started...)
    while True:
        try:
            urllib.request.urlopen(backends.get(
                'davical', {}).get("uri"), timeout=1)
        except urllib.error.HTTPError:
            break
        except urllib.error.URLError:
            pass

    yield backends.get('davical', {})
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml down".format(
            location=backends.get('davical', {}).get("location")),
        shell=True)
    time.sleep(3)  # wait for the container to stop


@contextlib.contextmanager
def davical_direct():
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    yield backends.get('davical2', {})


@contextlib.contextmanager
def xandikos_docker():
    check_docker()
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml up -d".format(
            location=backends.get('xandikos', {}).get("location")),
        shell=True)
    # TODO: instead of waiting a fixed time, check if caldav server is started with
    #       a http get loop for example
    time.sleep(5)  # wait for the container to starts
    yield backends.get('xandikos', {})
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml down".format(
            location=backends.get('xandikos', {}).get("location")),
        shell=True)
    time.sleep(3)  # wait for the container to stop


@contextlib.contextmanager
def xandikos_direct():
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    yield backends.get('xandikos2', {})



@contextlib.contextmanager
def cyrus_docker():
    check_docker()
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml up -d".format(
            location=backends.get('cyrus', {}).get("location")),
        shell=True)
    # TODO: instead of waiting a fixed time, check if caldav server is started with
    #       a http get loop for example
    time.sleep(5)  # wait for the container to starts
    yield backends.get('cyrus', {})
    subprocess.run(
        "docker-compose -f {location}/docker-compose.yml down".format(
            location=backends.get('cyrus', {}).get("location")),
        shell=True)
    time.sleep(3)  # wait for the container to stop


@contextlib.contextmanager
def cyrus_direct():
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    yield backends.get('cyrus2', {})



#@pytest.fixture(scope="session", params=['radicale', 'davical'])
@pytest.fixture(scope="session")
def backend(request):
    """Backend actually used."""
    # xandikos is not ready, it last some bug features like RRULE support, so we do
    # not test if for now.

    with cyrus_direct() as backend:
        yield backend

    # if request.param == 'radicale':
    #     with radicale_docker() as backend:
    #         yield backend
    # elif request.param == 'davical':
    #     with davical_docker() as backend:
    #         yield backend
    # elif request.param == 'xandikos':
    #     with xandikos_docker() as backend:
    #         yield backend
    # elif request.param == 'cyrus':
    #     with cyrus_docker() as backend:
    #         yield backend


@pytest.fixture(scope="function")
async def principal(request, event_loop, backend):
    """principal async fixture."""
    uri = backend.get('uri')
    # instead of a fixed login we generate a random one in order to start with an
    # empty principal.
    login = backend.get('login', uuid.uuid4().hex)
    password = backend.get('password', uuid.uuid4().hex)
    caldav = DAVClient(uri, username=login,
                       password=password, ssl_verify_cert=False)
    principal = await caldav.principal()

    def finalize():
        async def afin():
            await principal.prune()
        event_loop.run_until_complete(afin())
        
    request.addfinalizer(finalize)

    return principal


@pytest.fixture(scope="module", params=get_static_files_list('event'))
def event_fixtures(request):
    return get_one_static_file(request.param)


@pytest.fixture(scope="module")
def event1(request):
    return get_one_static_file("event_ok_caldav_1.ics", full_path=False)


@pytest.fixture(scope="module")
def event1bis(request):
    return get_one_static_file("event_ok_caldav_1bis.ics", full_path=False)


@pytest.fixture(scope="module")
def event2(request):
    return get_one_static_file("event_ok_caldav_2.ics", full_path=False)


@pytest.fixture(scope="module")
def event3(request):
    """Recurring event."""
    return get_one_static_file("event_ok_caldav_3.ics", full_path=False)


@pytest.fixture(scope="module", params=get_static_files_list('journal'))
def journal_fixtures(request):
    return get_one_static_file(request.param)


@pytest.fixture(scope="module", params=get_static_files_list('todo'))
def todo_fixtures(request):
    return get_one_static_file(request.param)
