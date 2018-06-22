import pytest

from aiocaldav.elements import cdav


def test_filter_1():
    """Should not raise an Error."""
    cdav.Filter().append(
        cdav.CompFilter("VCALENDAR").append(
            cdav.CompFilter("VEVENT").append(
                cdav.PropFilter("UID").append(
                    [cdav.TextMatch("pouet", negate=True)]))))
    assert True


def test_filter_2():
    crash = cdav.CompFilter()
    with pytest.raises(Exception):
        _ = str(crash)
