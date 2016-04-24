#!/usr/bin/env python
import sys
import requests
import re
import os
import codecs
import json
from datetime import datetime
from splinter import Browser
from fetch.http_cache import HttpCache
from fetch import brewery_db, sb, ip, rb
from utils import stdout_logger as logger
from utils.config import SB_SELECTOR_LIST, SB_SELECTORS_NAME, BROWSER_KWARGS


def main(sys_args):
    start_time = datetime.utcnow()
    beer_list = []
    beer_attrs = ('abv', 'alcohol', 'name', '^volume$', '^price$', 'sellstart', 'score', 'url',
                  'href', '^type$')

    def add_beer(b):
        if b and b.keys() > 0:
            beer_list.append({
                k: v for k, v in b.iteritems() if any([
                    a for a in beer_attrs if any(re.findall(a, k.lower()))
                ])
            })

    with requests.session() as session, Browser(**BROWSER_KWARGS) as browser:
        http = HttpCache(session, browser)
        logger.info('user-agent', requests.utils.default_user_agent())

        try:
            ip.ok(http)
        except RuntimeError as e:
            logger.err('ip', unicode(e.message))
            sys.exit(0)

        for style in rb.index_styles(http)[:21]:
            beers = rb.get_top_50_for_style(http, style['href'])
            for beer in beers:
                add_beer(beer)
                for b in brewery_db.find_by_name(http, beer.get('name')):
                    add_beer(b)

        name_0, name_1 = SB_SELECTORS_NAME

        for i in xrange(1, 2):
            response, next_page = sb.index_api_by_page(http, i)
            sb_list = response[SB_SELECTOR_LIST]
            for beer in sb_list:
                add_beer(beer)
                for b in brewery_db.find_by_name(http, name_0):
                    add_beer(b)
                for b in brewery_db.find_by_name(http, name_1):
                    add_beer(b)
                if not next_page:
                    break

        for site_map in sb.index_site_map(http):
            for site in sb.get_by_site_map(http, site_map):
                add_beer({'href': site})

        logger.info('duration', str((datetime.utcnow() - start_time).total_seconds()) + 's')

        filename = os.path.dirname(os.path.abspath(__file__)) + '/beers.json'
        with codecs.open(filename, 'w', 'utf-8') as file:
            logger.info('write', 'to ' + filename)
            file.truncate()
            file.write(unicode(json.dumps(beer_list, indent=2, ensure_ascii=False)))
        return 0


if __name__ == "__main__":
    main(sys.argv[1:])
