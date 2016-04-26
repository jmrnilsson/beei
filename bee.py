#!/usr/bin/env python
import sys
import requests
from datetime import datetime
from splinter import Browser
from fetch import brewery_db, sb, ip, rb
from utils import stdout_logger as logger
from utils.http_cache import HttpCache
from utils.beer_list import BeerList
from utils.config import SB_SELECTOR_LIST, SB_SELECTORS_NAME, BROWSER_KWARGS


def main(sys_args):
    start_time = datetime.utcnow()
    beer_list = BeerList()

    with requests.session() as session, Browser(**BROWSER_KWARGS) as browser:
        http = HttpCache(session, browser)
        logger.info('user-agent', requests.utils.default_user_agent())

        try:
            ip.ok(http)
        except RuntimeError as e:
            logger.err('ip', unicode(e.message))
            sys.exit(0)

        for style in rb.index_styles(http)[:37]:
            beers = rb.get_top_50_for_style(http, style['href'])
            for beer in beers:
                beer_list.add(beer)
                for b in brewery_db.find_by_name(http, beer.get('name')):
                    beer_list.add(b)

        for i in xrange(1, 10):
            api_index, next_page = sb.index_api_by_page(http, i)
            for beer in api_index[SB_SELECTOR_LIST]:
                beer_list.add(beer)
                names = [b for b in [beer[SB_SELECTORS_NAME[0]], beer[SB_SELECTORS_NAME[1]]] if b]
                for name in names:
                    for b in brewery_db.find_by_name(http, name):
                        beer_list.add(b)
            if not next_page:
                break

        for site_map in sb.index_site_map(http):
            for site in sb.get_by_site_map(http, site_map):
                beer_list.add({'href': site})

        beer_list.save()
        logger.info('duration', str((datetime.utcnow() - start_time).total_seconds()) + 's')
        return 0


if __name__ == "__main__":
    main(sys.argv[1:])
