#!/usr/bin/env python
import os
import sys
import codecs
import json
from datetime import datetime
from functional import seq

from utils import stdout_logger as logger


def main(sys_args):
    start_time = datetime.utcnow()
    filename = os.path.dirname(os.path.abspath(__file__)) + '/beers.json'

    if os.path.isfile(filename):
        with codecs.open(filename, 'r', 'utf-8') as file:
            logger.info('file', file)
            headers = [
                ("name_0", "Name"),
                ("name_1", "Name2"),
                ("price", "Price"),
                ("sale_start", "Sale start"),
                ("abv", "Alcohol"),
                ("supplier", "Supplier"),
                ("manufacturer", "Manufacturer")
                # ("organic", "Organic"),
                # ("category", "Category"),
                # ("ethical", "Ethical"),
                # ("koscher", "Koscher"),
            ]
            beers = seq.json(file)\
                .filter(lambda b: b.get('sale_start'))\
                .order_by(lambda b: datetime.strptime(b['sale_start'], '%Y-%m-%d'))\
                .reverse()\
                .take(25)\
                .cache()\
                .reverse()\
                .map(lambda b: {
                    k: unicode(v) for k, v in b.iteritems()
                    if k in [h[0] for h in headers]
                })\
                .to_list()
            logger.info('data', json.dumps(beers, indent=2, ensure_ascii=False))
    else:
        logger.error('file', '{} does not exists'.format(filename))

    logger.info('duration', str((datetime.utcnow() - start_time).total_seconds()) + 's')
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
