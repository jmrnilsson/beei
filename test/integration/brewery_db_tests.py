from nose.tools import assert_equal

from fetch import brewery_db


def test_find_by_id():
    actual = brewery_db.find_by_id('oeGSxs')
    assert_equal(actual['data']['name'], 'Naughty 90')


def test_find_by_name():
    actual = brewery_db.find_by_name('Naughty 90')
    assert_equal(actual['data'][0]['name'], 'Naughty 90')
