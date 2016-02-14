import requests
from nose.tools import assert_equal
from mock import Mock, patch
from utils import json_load_config
from fetch import sb as client


def response_mock():
    return Mock(json=Mock(return_value=json_load_config('response_sb.json')))


def test_find_all_by_page():
    with patch.object(requests, 'get', return_value=response_mock()):
        actual = client.find_all_by_page(1)
        product_number = actual['ProductSearchResults'][0]['ProductNumber']
        assert_equal(product_number, '8965101')
