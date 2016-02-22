from nose.tools import assert_is_not_none
from fetch import sb as client


def test_find_by_id():
    actual, _ = client.find_all_by_page(1)
    product_number = actual['ProductSearchResults'][0]['ProductNumber']
    assert_is_not_none(int(product_number))
