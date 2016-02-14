from nose.tools import assert_equal
from utils import get_logged_response


def test_json_response():
    response = get_logged_response('sb_response.json')
    next_product_number = response['ProductSearchResults'][0]['ProductNumber']
    assert_equal(next_product_number, '8965101')
