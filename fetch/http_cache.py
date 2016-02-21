import requests
import hashlib
import urllib
import json
import os.path
from datetime import datetime, timedelta
import re
import sys


class HttpCache:
    def __init__(self, session):
        self.session = session

    def get(self, url, cache_days, map_to=_map_json, params=None):
        url_params = url if not params else url + '?' + urllib.urlencode(params)
        site_hash = hashlib.sha1(url_params).hexdigest()
        url_words = re.findall('[0-9A-Za-z]{3,}', url)
        site = next(w for w in url_words if w not in ('https', 'http', 'www', 'dns', 'api'))
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        relative_file = '/logs/{}-{}.json'.format(site, site_hash)
        filename = path + relative_file

        if os.path.isfile(filename):
            modified = datetime.fromtimestamp(os.path.getmtime(filename))
            renewal = modified + timedelta(days=cache_days)
            if datetime.now() < renewal:
                with open(filename, 'r') as storage:
                    print >> sys.stdout, 'cached: .' + relative_file
                    return json.load(storage)

        response = self.session.get(url, params=params)
        response.raise_for_status()
        with open(filename, 'w') as storage:
            print >> sys.stdout, 'get: ' + filename
            result = map_to(response)
            storage.truncate()
            storage.write(json.dumps(result, indent=2))

        return result


def _map_json(response):
    return response.json()
