#!/usr/bin/env python
import sys
import requests

import config.sb as sb


def main(sys_args):
    r = requests.get(sb.get_url(33))

    return r.text


if __name__ == "__main__":
    print main(sys.argv[1:])
