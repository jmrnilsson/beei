import os
import inspect
import json
from nose.tools import assert_is_not_none, assert_equal

from beei import main


def test_main():
    assert_is_not_none(main(None))


def test_json_response():
    next_product_number = get_page()['ProductSearchResults'][0]['ProductNumber']
    assert_equal(next_product_number, '8965101')


def get_page():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    temp_path = os.path.dirname(path + '/../../config/')
    with open(temp_path + '/sb_response.json') as input_parameters:
        return json.load(input_parameters)
