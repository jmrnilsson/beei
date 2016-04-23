import hashlib
import urllib
import json
import os
from datetime import datetime, timedelta
from random import randint
import time
import re
from utils import stdout_logger as logger

class HttpCache:
    def __init__(self, session):
        self.session = session
        self.throttle_lock = {}

    def _cache(self, cache_days, fetch, url, params=None):
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
                    logger.info('cached', *self._short_name(filename))
                    return json.load(file)

        throttle_lock_time = datetime.utcnow()
        if self.throttle_lock.get(site):
            throttle_lock_time = self.throttle_lock.pop(site) + timedelta(seconds=3 + randint(0, 15))

        while (datetime.utcnow() < throttle_lock_time):
            time.sleep(1)

        self.throttle_lock[site] = datetime.utcnow()
        result = fetch()

        with open(filename, 'w') as file:
            logger.warn('get', *self._short_name(filename))
            file.truncate()
            file.write(json.dumps(result, indent=2))

        return result

    @staticmethod
    def _short_name(filename):
        # too lazy to split regex for now
        return re.findall(r'(?<=\/)\w{3,}\-\w{3,}(?=\.json)', filename)[0].split('-')

    def get(self, cache_days, url, params=None, map_to=lambda r: r.json()):
        def fetch():
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return map_to(response)
        return self._cache(cache_days, fetch, url, params=params)

    def visit(self, cache_days, url, fetch):
        return self._cache(cache_days, fetch, url)
