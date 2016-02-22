import requests
from fetch.http_cache import HttpCache
from nose.tools import assert_raises, assert_is_not_none
from fetch.ip import *


def test_check():
    with requests.session() as session:
        http = HttpCache(session)
        actual = check(http)['ip']
        assert_is_not_none(int(actual[:1]))


# Move to unit test
def _test_not_ok():
    with requests.session() as session:
        http = HttpCache(session)
        assert_raises(RuntimeError, ok, http)
