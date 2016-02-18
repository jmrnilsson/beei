#!/usr/bin/env python
import sys
from fetch import brewery_db
from fetch import sb
import fetch.ip as ip
from utils import sb_name_0, sb_name_1, sb_list


def main(sys_args):
    if not ip.ok():
        return 1

    for i in xrange(1, 20):
        b_list = sb.find_all_by_page(i)[sb_list()]
        print >> sys.stdout, 'add: ' + unicode(len(b_list))
        for b in b_list:
            name_0 = b.get(sb_name_0())
            name_1 = b.get(sb_name_1())
            if name_0:
                brewery_db.find_by_name(name_0)
            if name_1:
                brewery_db.find_by_name(name_1)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
