"""Fixtures for tests."""
import contextlib
import glob
import os
import subprocess
import time

import pytest

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


@contextlib.contextmanager
def radicale_docker():
    # TODO: use pkg_resource to discover the good path of the docker-compose file.
    try:
        subprocess.run("docker ps", shell=True).check_returncode()
    except subprocess.CalledProcessError:
        raise Exception(
            "Docker seems not started. Start it before running tests")
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


@pytest.fixture(scope="module")
def backend(request):
    with radicale_direct() as backend:
        yield backend


@pytest.fixture(scope="module", params=get_static_files_list('event'))
def event_fixtures(request):
    return get_one_static_file(request.param)


@pytest.fixture(scope="module")
def event1(request):
    return get_one_static_file("event_ok_caldav_1.ics", full_path=False)


@pytest.fixture(scope="module")
def event2(request):
    return get_one_static_file("event_ok_caldav_2.ics", full_path=False)


@pytest.fixture(scope="module", params=get_static_files_list('journal'))
def journal_fixtures(request):
    return get_one_static_file(request.param)


@pytest.fixture(scope="module", params=get_static_files_list('todo'))
def todo_fixtures(request):
    return get_one_static_file(request.param)
