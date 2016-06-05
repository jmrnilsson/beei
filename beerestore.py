#!/usr/bin/env python
import sys
import requests
from datetime import datetime
from splinter import Browser
from fetch import brewery_db, s, ip, rb
from utils import stdout_logger as logger
from utils.http_cache import HttpCache
from utils.beer_list import BeerList
from utils.config import BROWSER_KWARGS, USER_AGENT


def main(sys_args):
    start_time = datetime.utcnow()
    beer_list = BeerList()

    with requests.session() as session, Browser(**BROWSER_KWARGS) as browser:
        http = HttpCache(session, browser)
        logger.info('user-agent', USER_AGENT or requests.utils.default_user_agent())

        try:
            ip.ok(http)
        except RuntimeError as e:
            logger.err('ip', unicode(e.message))
            sys.exit(0)

        for beer in s.api_get_all(http):
            beer_list.add(beer)
            # for name in [b for b in [beer['name_0'], beer['name_1']] if b]:
            # for b in brewery_db.find_by_name(http, name):
            #     beer_list.add(b)

        for beer in rb.get_all(http):
            beer_list.add(beer)

    beer_list.save()
    logger.info('duration', '{:.3f}s'.format((datetime.utcnow() - start_time).total_seconds()))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
