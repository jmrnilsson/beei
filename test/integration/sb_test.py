from nose.tools import assert_equal
from fetch import sb as client


def test_find_by_id():
    actual = client.find_all_by_page(1)
    product_number = actual['ProductSearchResults'][0]['ProductNumber']
    assert_equal(product_number[:3], '305')
