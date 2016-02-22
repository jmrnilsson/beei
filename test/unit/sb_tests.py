from fetch.http_cache import HttpCache
from nose.tools import assert_equal
from mock import patch
from utils import json_load_config
from fetch import sb as client


def test_find_all_by_page():
    with patch.object(HttpCache, 'get', return_value=json_load_config('response_sb.json')):
        actual = client.find_all_by_page(HttpCache(None), 1)
        product_number = actual['ProductSearchResults'][0]['ProductNumber']
        assert_equal(product_number, '8965101')
