"""Fixtures for tests."""
import contextlib
import subprocess
import time

import pytest

from .conf import backends


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
    with radicale_docker() as backend:
        yield backend


@pytest.fixture(scope="module", params=[1, 2, 3])
def event1(request):
    if request.param == 1:
        return """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:20010712T182145Z-123401@example.com
DTSTAMP:20060712T182145Z
DTSTART:20060714T170000Z
DTEND:20060715T040000Z
SUMMARY:Bastille Day Party
END:VEVENT
END:VCALENDAR
"""
    elif request.param == 2:
        return """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:20010712T182145Z-123401@example.com
DTSTAMP:20070712T182145Z
DTSTART:20070714T170000Z
DTEND:20070715T040000Z
SUMMARY:Bastille Day Party +1year
END:VEVENT
END:VCALENDAR
"""
    elif request.param == 3:
        # example from http://www.rfc-editor.org/rfc/rfc5545.txt
        return """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:19970901T130000Z-123403@example.com
DTSTAMP:19970901T130000Z
DTSTART;VALUE=DATE:19971102
SUMMARY:Our Blissful Anniversary
TRANSP:TRANSPARENT
CLASS:CONFIDENTIAL
CATEGORIES:ANNIVERSARY,PERSONAL,SPECIAL OCCASION
RRULE:FREQ=YEARLY
END:VEVENT
END:VCALENDAR"""


@pytest.fixture(scope="module")
def journal1(request):
    # example from http://www.kanzaki.com/docs/ical/vjournal.html
    return """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VJOURNAL
UID:19970901T130000Z-123405@example.com
DTSTAMP:19970901T130000Z
DTSTART;VALUE=DATE:19970317
SUMMARY:Staff meeting minutes
DESCRIPTION:1. Staff meeting: Participants include Joe\, Lisa
  and Bob. Aurora project plans were reviewed. There is currently
  no budget reserves for this project. Lisa will escalate to
  management. Next meeting on Tuesday.\n
END:VJOURNAL
END:VCALENDAR
"""


@pytest.fixture(scope="module", params=[1, 2, 3, 4])
def todo1(request):
    if request.param == 1:
        # example from http: // www.rfc-editor.org/rfc/rfc5545.txt
        return """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VTODO
UID:20070313T123432Z-456553@example.com
DTSTAMP:20070313T123432Z
DUE;VALUE=DATE:20070501
SUMMARY:Submit Quebec Income Tax Return for 2006
CLASS:CONFIDENTIAL
CATEGORIES:FAMILY,FINANCE
STATUS:NEEDS-ACTION
END:VTODO
END:VCALENDAR"""
    elif request.param == 2:
        # example from RFC2445, 4.6.2
        return """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VTODO
UID:19970901T130000Z-123404@host.com
DTSTAMP:19970901T130000Z
DTSTART:19970415T133000Z
DUE:19970416T045959Z
SUMMARY:1996 Income Tax Preparation
CLASS:CONFIDENTIAL
CATEGORIES:FAMILY,FINANCE
PRIORITY:2
STATUS:NEEDS-ACTION
END:VTODO
END:VCALENDAR"""
    elif request.param == 3:
        return """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VTODO
UID:19970901T130000Z-123405@host.com
DTSTAMP:19970901T130000Z
DTSTART:19970415T133000Z
DUE:19970516T045959Z
SUMMARY:1996 Income Tax Preparation
CLASS:CONFIDENTIAL
CATEGORIES:FAMILY,FINANCE
PRIORITY:1
STATUS:NEEDS-ACTION
END:VTODO
END:VCALENDAR"""
    elif request.param == 4:
        return """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VTODO
UID:19970901T130000Z-123406@host.com
DTSTAMP:19970901T130000Z
SUMMARY:1996 Income Tax Preparation
CLASS:CONFIDENTIAL
CATEGORIES:FAMILY,FINANCE
PRIORITY:1
STATUS:NEEDS-ACTION
END:VTODO
END:VCALENDAR"""
