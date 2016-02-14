from nose.tools import assert_equal
from utils import json_load_config


def test_json_response():
    response = json_load_config('response_sb.json')
    next_product_number = response['ProductSearchResults'][0]['ProductNumber']
    assert_equal(next_product_number, '8965101')
