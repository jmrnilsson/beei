#!/usr/bin/env python
import sys
import requests
from datetime import datetime
from splinter import Browser
from fetch.http_cache import HttpCache
from fetch import brewery_db, sb, ip, rb
from utils import stdout_logger as logger
from utils.config import SB_SELECTOR_LIST, SB_SELECTORS_NAME, BROWSER_KWARGS


def main(sys_args):
    start_time = datetime.utcnow()
    with requests.session() as session, Browser(**BROWSER_KWARGS) as browser:
        http = HttpCache(session, browser)
        logger.info('user-agent', requests.utils.default_user_agent())

        try:
            ip.ok(http)
        except RuntimeError as e:
            logger.err('ip', unicode(e.message))
            sys.exit(0)

        for style in rb.index(http)[:7]:
            beers = rb.get_top_50_for_style(http, style['href'])
            for beer in beers:
                find_all_by_name(http, beer.get('name'))

        name_0, name_1 = SB_SELECTORS_NAME

        for i in xrange(1, 2):
            response, next_page = sb.find_all_by_page(http, i)
            sb_list = response[SB_SELECTOR_LIST]
            for beer in sb_list:
                # find_all_by_name(http, beer.get(name_0), beer.get(name_1))
                if not next_page:
                    break
        logger.info('duration', str((datetime.utcnow() - start_time).total_seconds()) + 's')
        return 0


def find_all_by_name(http, *args):
    for name in args:
        if name in (None, ''):
            continue
        logger.info('name', name[:15])
        brewery_db.find_by_name(http, name)


if __name__ == "__main__":
    main(sys.argv[1:])
