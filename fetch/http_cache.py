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
    def __init__(self, session, browser):
        self.session = session
        self.browser = browser
        self.throttle_lock = {}

    def _log_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/logs/'

    def _cache(self, cache_days, fetch, url, params=None):
        url_params = url if not params else url + '?' + urllib.urlencode(params)
        url_hash = hashlib.sha1(url_params).hexdigest()
        words = re.findall('\w{3,}', url)
        site = next(w for w in words if w not in ('https', 'http', 'www', 'dns', 'api'))
        filename = self._log_path() + '{}-{}.json'.format(site, url_hash)

        # reverse proxy (web accel)
        if os.path.isfile(filename):
            modified = datetime.fromtimestamp(os.path.getmtime(filename))
            invalidation_time = modified + timedelta(days=cache_days)
            if datetime.now() < invalidation_time:
                with open(filename, 'r') as file:
                    logger.info('cached', *self._short_name(filename).split('-'))
                    return json.load(file)

        # avoid throttling
        if self.throttle_lock.get(site):
            total_lock_time = (datetime.utcnow() - self.throttle_lock.pop(site)).total_seconds()
            delay = timedelta(seconds=3 + randint(0, 7)).total_seconds()
            time.sleep(max(delay - total_lock_time, 0))

        # request
        self.throttle_lock[site] = datetime.utcnow()
        result = fetch()

        # local store
        with open(filename, 'w') as file:
            logger.warn('get', *self._short_name(filename).split('-'))
            file.truncate()
            file.write(json.dumps(result, indent=2))

        return result

    @staticmethod
    def _short_name(filename):
        return re.findall(r'(?<=\/)\w{3,}\-\w{3,}(?=\.json)', filename)[0]

    def get(self, cache_days, url, params=None, map_to=lambda r: r.json()):
        def fetch():
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return map_to(response)
        return self._cache(cache_days, fetch, url, params=params)

    def visit(self, cache_days, url, map_to=None):
        def fetch():
            self.browser.visit(url)
            return map_to(self.browser)
        return self._cache(cache_days, fetch, url)
