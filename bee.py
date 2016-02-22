#!/usr/bin/env python
import sys
import requests
from fetch.http_cache import HttpCache
from fetch import brewery_db, sb, ip
from utils import sb_name_0, sb_name_1, sb_list


def main(sys_args):
    with requests.session() as session:
        http = HttpCache(session)

        if not ip.ok(http):
            return 1

        for i in xrange(1, 25):
            print >> sys.stdout, 'user-agent: ' + requests.utils.default_user_agent()
            b_list = sb.find_all_by_page(http, i)[sb_list()]
            print >> sys.stdout, 'add: ' + unicode(len(b_list))
            for b in b_list:
                name_0 = b.get(http, sb_name_0())
                name_1 = b.get(http, sb_name_1())
                if name_0:
                    brewery_db.find_by_name(http, name_0)
                if name_1:
                    brewery_db.find_by_name(http, name_1)

        return 0


if __name__ == "__main__":
    main(sys.argv[1:])
