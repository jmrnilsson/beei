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

    def get(self, cache_days, url, params=None, map_to=lambda r: r.json()):
        url_params = url if not params else url + '?' + urllib.urlencode(params)
        site_hash = hashlib.sha1(url_params).hexdigest()
        url_words = re.findall('\w{3,}', url)
        site = next(w for w in url_words if w not in ('https', 'http', 'www', 'dns', 'api'))
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/logs/'
        filename = path + '{}-{}.json'.format(site, site_hash)

        if os.path.isfile(filename):
            modified = datetime.fromtimestamp(os.path.getmtime(filename))
            renewal = modified + timedelta(days=cache_days)
            if datetime.now() < renewal:
                with open(filename, 'r') as file:
                    print >> sys.stdout, 'cached: '.ljust(10, ' ') + self._short_name(filename)
                    return json.load(file)

        response = self.session.get(url, params=params)
        response.raise_for_status()

        with open(filename, 'w') as file:
            print >> sys.stdout, 'get: '.ljust(10, ' ') + self._short_name(filename)
            result = map_to(response)
            file.truncate()
            file.write(json.dumps(result, indent=2))

        return result

    def _short_name(self, filename):
        return re.findall(r'(?<=\/)\w{3,}\-\w{3,}(?=\.json)', filename)[0]
