from nose.tools import assert_greater, assert_equal, assert_raises
from fetch.ip_check import find_all_void_ips, check_ip, assert_ok_ip


def test_find_all_invalid_ip_addresses():
    actual = find_all_void_ips()
    assert_greater(len(actual), 25)
    assert_equal(actual[0]['start'][:2], '2.')


def test_check_ip():
    actual = check_ip()
    assert_equal(actual['ip'][:1], '8')


def test_nok_ip():
    assert_raises(RuntimeError, assert_ok_ip)
