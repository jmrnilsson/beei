from nose.tools import assert_greater, assert_equal
from fetch.ip_check import find_all_invalid_ip_addresses, check_ip


def test_find_all_invalid_ip_addresses():
    actual = find_all_invalid_ip_addresses()
    assert_greater(len(actual), 25)
    assert_equal(actual[0]['start'][:1], '0')


def test_check_ip():
    actual = check_ip()
    assert_equal(actual['ip'][:1], '0')