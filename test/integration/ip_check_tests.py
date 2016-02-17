from nose.tools import assert_greater, assert_equal, assert_raises, assert_is_not_none
from fetch.ip import *


def test_find_all_void():
    actual = find_all_void()
    assert_greater(len(actual), 25)
    assert_is_not_none(int(actual[0]['start'][:1]))


def test_check():
    actual = check()
    assert_is_not_none(int(actual[:1]))


# Move to unit test
def _test_not_ok():
    assert_raises(RuntimeError, ok)
