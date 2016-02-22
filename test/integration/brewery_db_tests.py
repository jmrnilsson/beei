from nose.tools import assert_equal
import requests
from fetch.http_cache import HttpCache
from fetch import brewery_db


def test_find_by_id():
    with requests.session() as session:
        http = HttpCache(session)
        actual = brewery_db.find_by_id(http, 'oeGSxs')
        assert_equal(actual['data']['name'], 'Naughty 90')


def test_find_by_name():
    with requests.session() as session:
        http = HttpCache(session)
        actual = brewery_db.find_by_name(http, 'Naughty 90')
        assert_equal(actual['data'][0]['name'], 'Naughty 90')
