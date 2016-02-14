#!/usr/bin/env python
import sys
import requests
import json

import config.sb as sb


def main(sys_args):
    # r = requests.get(sb.get_url(1))
    # return json.load(r.text)
    return '0'


if __name__ == "__main__":
    print main(sys.argv[1:])
