from nose.tools import assert_greater, assert_equal, assert_raises, assert_is_not_none
from fetch.ip_check import find_all_void_ips, check_ip, assert_ok_ip


def test_find_all_invalid_ip_addresses():
    actual = find_all_void_ips()
    assert_greater(len(actual), 25)
    assert_is_not_none(int(actual[0]['start'][:1]))


def test_check_ip():
    actual = check_ip()
    assert_is_not_none(int(actual[:1]))


# Move to unit test
def _test_nok_ip():
    assert_raises(RuntimeError, assert_ok_ip)
