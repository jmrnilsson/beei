#!/usr/bin/env python
import os
import sys
import codecs
import json
from datetime import datetime, timedelta
from functional import seq
import requests

from fetch import brewery_db
from utils import stdout_logger as logger
from utils.http_cache import HttpCache


def main(sys_args):
    weeks, = sys_args or [21]
    start_time = datetime.utcnow()
    from_date = (start_time - timedelta(int(weeks))).date()
    count = 0
    filename = os.path.dirname(os.path.abspath(__file__)) + '/beers.json'

    if os.path.isfile(filename):
        with codecs.open(filename, 'r', 'utf-8') as file:
            logger.info('file', filename)
            headers = [
                ("name_0", "Name"),
                ("name_1", "Name2"),
                ("price", "Price"),
                ("sale_start", "Sale start"),
                ("abv", "Alcohol"),
                ("supplier", "Supplier"),
                ("manufacturer", "Manufacturer")
            ]

            beers = _get_beers_with_sale_start(file, from_date, headers)
            ratings = _get_ratings(file)
            _apply_ratings_to_beers(beers, ratings)
            logger.info('data', json.dumps(beers, indent=2, ensure_ascii=False))
            count += len(beers)
    else:
        logger.error('file', '{} does not exists'.format(filename))

    logger.info('count', 'found {} since {:%Y-%m-%d %H:%M}'.format(count, from_date))
    logger.info('duration', '{:.3f}s'.format((datetime.utcnow() - start_time).total_seconds()))
    return 0


def _strpdate(date_text):
    return datetime.strptime(date_text, '%Y-%m-%d').date()


def _get_beers_with_sale_start(file, from_date, headers):
    file.seek(0)
    return seq.json(file)\
        .filter(lambda b: b.get('sale_start') and _strpdate(b['sale_start']) > from_date)\
        .sorted(key=lambda b: _strpdate(b['sale_start']), reverse=True)\
        .take(30)\
        .cache()\
        .reverse()\
        .map(lambda b: {
            k: unicode(v) for k, v in b.iteritems()
            if k in [h[0] for h in headers]
        })\
        .to_list()


def _get_ratings(file):
    file.seek(0)
    return seq.json(file).filter(lambda b: b.get('rate'))


def _apply_ratings_to_beers(beers, ratings):
    with requests.session() as session:
        http = HttpCache(session, None)

        for beer in beers:
            for n in ('name_0', 'name_1'):
                brewery_db.apply_if_find_single_by_name(http, beer, n, beer.update)
                _apply_rb(ratings, beer, n, beer.update)


def _apply_rb(ratings_seq, beer, key_name, func):
    def in_str(expression, text):
        def _lower_trim(text):
            return text.lower().replace(' ', '')
        return _lower_trim(expression) in _lower_trim(text)

    rating = ratings_seq.filter(lambda r: in_str(beer[key_name], r['name'])).to_list()

    if rating:
        func({
            'rb-{1}-{0}'.format(k, key_name): v
            for k, v in rating[0].iteritems()
            if isinstance(v, basestring)
        })

if __name__ == "__main__":
    main(sys.argv[1:])
