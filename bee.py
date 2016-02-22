#!/usr/bin/env python
import sys
import requests
from fetch.http_cache import HttpCache
from fetch import brewery_db, sb, ip
from utils import sb_name_0, sb_name_1, sb_list


def main(sys_args):
    with requests.session() as session:
        http = HttpCache(session)
        print >> sys.stdout, 'user-agent: '.ljust(10, ' ') + requests.utils.default_user_agent()

        if not ip.ok(http):
            return 1

        for i in xrange(1, 35):
            response, next_page = sb.find_all_by_page(http, i)
            b_list = response[sb_list()]
            print >> sys.stdout, 'add: '.ljust(10, ' ') + unicode(len(b_list))
            for b in b_list:
                name_0 = b.get(sb_name_0())
                name_1 = b.get(sb_name_1())
                if name_0:
                    brewery_db.find_by_name(http, name_0)
                if name_1:
                    brewery_db.find_by_name(http, name_1)
                if not next_page:
                    break

        return 0


if __name__ == "__main__":
    main(sys.argv[1:])
