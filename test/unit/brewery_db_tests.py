import requests
from nose.tools import assert_equal, with_setup
from mock import Mock
from fetch import brewery_db
from utils import get_logged_response

original_requests_get = requests.get


def set_up():
    response = Mock()
    response.json = Mock(return_value=get_logged_response('brewery_db_response.json'))
    requests.get = Mock(return_value=response)


def tear_down():
    requests.get = original_requests_get


@with_setup(set_up, tear_down)
def test_find_by_id():
    actual = brewery_db.find_by_id('oeGSxs')
    assert_equal(actual['data']['name'], 'Naughty 90')
