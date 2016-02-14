import requests
from nose.tools import assert_equal
from mock import Mock, patch
from fetch import brewery_db as client
from utils import json_load_config


def response_mock():
    return Mock(json=Mock(return_value=json_load_config('response_brewery_db.json')))


def test_find_by_id():
    with patch.object(requests, 'get', return_value=response_mock()):
        actual = client.find_by_id('oeGSxs')
        assert_equal(actual['data']['name'], 'Naughty 91')
