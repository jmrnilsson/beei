#!/usr/bin/env python
import sys
import requests
from fetch.http_cache import HttpCache
from fetch import brewery_db, sb, ip, rb
from utils import stdout_logger as logger
from utils.config import SB_SELECTOR_LIST, SB_SELECTORS_NAME


def main(sys_args):
    with requests.session() as session:
        http = HttpCache(session)
        logger.info('user-agent', requests.utils.default_user_agent())

        try:
            ip.ok(http)
        except RuntimeError as e:
            logger.err('ip', unicode(e.message))
            sys.exit(0)

        rb.index(http)
        name_sel_0, name_sel_1 = SB_SELECTORS_NAME

        for i in xrange(1, 35):
            response, next_page = sb.find_all_by_page(http, i)
            sb_list = response[SB_SELECTOR_LIST]
            logger.info('add', unicode(len(sb_list)) + ' more records')
            for b in sb_list:
                '''
                find_all_by_name(http, b.get(name_sel_0), b.get(name_sel_1))
                if not next_page:
                    break
                '''

        return 0


def find_all_by_name(http, *args):
    for name in args:
        if name in (None, ''):
            continue
        logger.info('name', name)
        brewery_db.find_by_name(http, name)


if __name__ == "__main__":
    main(sys.argv[1:])
