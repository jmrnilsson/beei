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
            beers = seq.json(file)\
                .filter(lambda b: b.get('sale_start') and _strpdate(b['sale_start']) > from_date)\
                .sorted(key=lambda b: _strpdate(b['sale_start']), reverse=True)\
                .take(25)\
                .cache()\
                .reverse()\
                .map(lambda b: {
                    k: unicode(v) for k, v in b.iteritems()
                    if k in [h[0] for h in headers]
                })\
                .to_list()

            file.seek(0)
            ratings = seq.json(file).filter(lambda b: b.get('rate'))

            with requests.session() as session:
                http = HttpCache(session, None)

                for beer in beers:
                    rating = ratings.filter(
                        lambda r: r['name'].lower() == beer['name_0'].lower()
                    ).to_list()
                    rating1 = ratings.filter(
                        lambda r: r['name'].lower() == beer['name_1'].lower()
                    ).to_list()
                    brewery_db.apply_if_find_single_by_name(http, beer, 'name_0', beer.update)
                    brewery_db.apply_if_find_single_by_name(http, beer, 'name_1', beer.update)

                    if rating:
                        beer.update(rating[0])
                    if rating1:
                        beer.update(rating1[0])

            logger.info('data', json.dumps(beers, indent=2, ensure_ascii=False))
            count += len(beers)
    else:
        logger.error('file', '{} does not exists'.format(filename))

    logger.info('count', 'found {} since {:%Y-%m-%d %H:%M}'.format(count, from_date))
    logger.info('duration', '{:.3f}s'.format((datetime.utcnow() - start_time).total_seconds()))
    return 0


def _strpdate(date_text):
    return datetime.strptime(date_text, '%Y-%m-%d').date()


if __name__ == "__main__":
    main(sys.argv[1:])
