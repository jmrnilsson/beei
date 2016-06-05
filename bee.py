#!/usr/bin/env python
import os
import sys
import codecs
import json
from datetime import datetime

from utils import stdout_logger as logger


def main(sys_args):
    start_time = datetime.utcnow()
    filename = os.path.dirname(os.path.abspath(__file__)) + '/beers.json'

    if os.path.isfile(filename):
        with codecs.open(filename, 'r', 'utf-8') as file:
            logger.info('file', file)
            loaded = json.load(file)
            filtered = filter(lambda b: b.get('sale_start'), loaded)
            sort = sorted(filtered, key=lambda b: datetime.strptime(b['sale_start'], '%Y-%m-%d'), reverse=True)
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
            mapped = [
                {
                    k: unicode(v) for k, v in b.iteritems()
                    if k in [h[0] for h in headers]
                }
                for b in reversed(sort[:25])
            ]
            logger.info('data', json.dumps(mapped, indent=2, ensure_ascii=False))
    else:
        logger.error('file', '{} does not exists'.format(filename))

    logger.info('duration', str((datetime.utcnow() - start_time).total_seconds()) + 's')
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
