import pytest
import scraper.handleNLP as handleNLP
import time


def test_add():
    res = handleNLP.add(1, 4)
    assert res == 5


def test_add_strings():
    assert handleNLP.add("a", "b") == "ab"


def test_divide():
    res = handleNLP.divide(10, 5)
    assert res == 2


def test_divide_by_zero():
    with pytest.raises(ValueError):
        handleNLP.divide(10, 0)

@pytest.mark.slow
@pytest.mark.filterwarnings('ignore::pytest.PytestUnknownMarkWarning')
def test_very_slow():
    time.sleep(1)
    res = handleNLP.divide(10, 5)
    assert res == 2


@pytest.mark.skip(reason='feature is broken')
def test_add():
    assert handleNLP.add(1, 2) == 3


@pytest.mark.xfail(reason='we know we cant divide by 0')
def test_test_divide_by_zero_broken():
    with pytest.raises(ValueError):
        handleNLP.divide(10, 0)

