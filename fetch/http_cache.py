import requests
import hashlib
import urllib
import json
import os.path
import inspect
from datetime import datetime, timedelta
import re
import bee


class HttpCache:
    def __init__(self, cache_days, map_to=None):
        self.cache_days = cache_days
        self.map_to = map_to if map else self._map_json

    def get(self, url, params=None):
        url_params = url if not params else url + '?' + urllib.urlencode(params)
        site_hash = hashlib.sha1(url_params).hexdigest()
        url_words = re.findall('[0-9A-Za-z]{3,}', url)
        site = next(w for w in url_words if w not in ('https', 'http', 'www', 'dns', 'api'))
        path = os.path.dirname(os.path.abspath(inspect.getfile(bee)))
        filename = '{}/logs/{}-{}.json'.format(path, site, site_hash)

        if os.path.isfile(filename):
            modified = datetime.fromtimestamp(os.path.getmtime(filename))
            renewal = modified + timedelta(days=self.cache_days)
            if datetime.now() < renewal:
                with open(filename, 'r') as storage:
                    return json.load(storage)

        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(filename, 'w') as storage:
            result = self.map_to(response)
            storage.truncate()
            storage.write(json.dumps(result, indent=2))

        return result

    @staticmethod
    def _map_json(response):
        return response.json()