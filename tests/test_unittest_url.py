"""Exercising the URL class"""
from urllib.parse import urlparse

import pytest

from aiocaldav.lib.url import URL

LONG_URL = "http://foo:bar@www.example.com:8080/caldav.php/?foo=bar"


@pytest.fixture(scope="module")
def url0(request):
    return URL.objectify(None)


@pytest.fixture(scope="module")
def url0b(request):
    return URL.objectify("")


@pytest.fixture(scope="module")
def url1(request):
    return URL.objectify(LONG_URL)


@pytest.fixture(scope="module")
def url3(request):
    return URL.objectify("/bar")


@pytest.fixture(scope="module")
def url5(request):
    return URL.objectify(urlparse("/bar"))


def test_url_1(url1):
    # 1) URL.objectify should return a valid URL object almost no matter
    # what's thrown in
    url2 = URL.objectify(url1)
    assert url1 == url2
    assert url2.path == '/caldav.php/'


def test_url_2(url1):
    url4 = URL.objectify(urlparse(str(url1)))
    assert url1 == url4


def test_url_3(url3, url5):
    assert url3 == url5


def test_url_4(url1):
    # 3) str will always return the URL
    assert str(url1) == LONG_URL


def test_url_5(url3):
    assert str(url3) == "/bar"


def test_url_6(url1):
    url4 = URL.objectify(urlparse(str(url1)))
    assert str(url4) == LONG_URL


def test_url_7(url5):
    assert str(url5) == "/bar"


def test_url_7bis(url5):
    assert url5.path == '/bar'


def test_url_8(url1):
    # 4) join method
    url2 = URL.objectify(url1)
    url6 = url1.join(url2)
    assert url6 == url1


def test_url_9(url1, url3):
    url7 = url1.join(url3)
    assert url7 == "http://foo:bar@www.example.com:8080/bar"


def test_url_10(url1):
    url4 = URL.objectify(urlparse(str(url1)))
    url8 = url1.join(url4)
    assert url8 == url1


def test_url_11(url1, url3, url5):
    url7 = url1.join(url3)
    url9 = url1.join(url5)
    assert url9 == url7


def test_url_12(url1):
    urlA = url1.join("someuser/calendar")
    assert urlA == "http://foo:bar@www.example.com:8080/caldav.php/someuser/calendar"


def test_url_13(url1, url5):
    urlB = url5.join(url1)
    assert urlB == url1


def test_url_14(url1):
    with pytest.raises(ValueError):
        url1.join("http://www.google.com")


def test_url_15(url0, url0b, url1):
    # 4b) join method, with URL as input parameter
    url2 = URL.objectify(url1)
    url6 = url1.join(URL.objectify(url2))
    assert url6 == url1

    url6b = url6.join(url0)
    url6c = url6.join(url0b)

    url6d = url6.join(None)
    for url6alt in (url6b, url6c, url6d):
        assert url6 == url6alt


def test_url_16(url1, url3):
    url7 = url1.join(URL.objectify(url3))
    assert url7 == "http://foo:bar@www.example.com:8080/bar"
    assert url7.username == 'foo'
    assert url7.is_auth() is True
    # 7) unauth() strips username/password
    assert url7.unauth() == 'http://www.example.com:8080/bar'


def test_url_17(url1):
    url4 = URL.objectify(urlparse(str(url1)))
    url8 = url1.join(URL.objectify(url4))
    assert url8 == url1


def test_url_18(url1, url5):
    url9 = url1.join(URL.objectify(url5))
    assert url9 == "http://foo:bar@www.example.com:8080/bar"


def test_url_19(url1):
    urlA = url1.join(URL.objectify("someuser/calendar"))
    assert urlA == "http://foo:bar@www.example.com:8080/caldav.php/someuser/calendar"


def test_url_20(url1, url5):
    urlB = url5.join(URL.objectify(url1))
    assert urlB == url1


def test_url_21(url1):
    # 5) all urlparse methods will work.  always.
    assert url1.scheme == 'http'


def test_url_22(url1):
    urlC = URL.objectify("https://www.example.com:443/foo")
    assert urlC.port == 443

    # 6) is_auth returns True if the URL contains a username.
    assert urlC.is_auth() is False
