import requests
from fetch.http_cache import HttpCache
from nose.tools import assert_is_not_none
from fetch import sb as client


def test_find_by_id():
    with requests.session() as session:
        http = HttpCache(session)
        actual = client.find_all_by_page(http, 1)
        product_number = actual['ProductSearchResults'][0]['ProductNumber']
        assert_is_not_none(int(product_number))
