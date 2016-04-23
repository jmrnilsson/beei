#!/usr/bin/env python
import sys
import requests
from fetch.http_cache import HttpCache
from fetch import brewery_db, sb, ip, rb
from utils import config, info, err


def main(sys_args):
    with requests.session() as session:
        http = HttpCache(session)
        info('user-agent', requests.utils.default_user_agent())

        try:
            ip.ok(http)
        except RuntimeError as e:
            err('ip', unicode(e.message))
            sys.exit(0)

        rb.index(http)

        for i in xrange(1, 20):
            response, next_page = sb.find_all_by_page(http, i)
            b_list = response[config.sb_list()]
            info('add', unicode(len(b_list)))
            for b in b_list:
                find_all_by_name(http, b.get(config.sb_name_0()), b.get(config.sb_name_1()))
                if not next_page:
                    break

        return 0


def find_all_by_name(http, *args):
    for name in args:
        if name in (None, ''):
            continue
        info('name', name)
        brewery_db.find_by_name(http, name)


if __name__ == "__main__":
    main(sys.argv[1:])
