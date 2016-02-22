from fetch.http_cache import HttpCache
from nose.tools import assert_equal
from mock import patch
from fetch import brewery_db as client
from utils import json_load_config


def test_find_by_id():
    with patch.object(HttpCache, 'get', return_value=json_load_config('response_brewery_db.json')):
        actual = client.find_by_id(HttpCache(None), 'oeGSxs')
        assert_equal(actual['data']['name'], 'Naughty 91')
