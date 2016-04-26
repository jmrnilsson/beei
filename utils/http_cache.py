import hashlib
import urllib
import json
import os
from datetime import datetime, timedelta
from random import randint
import time
import re
import codecs
import robotparser
from utils import stdout_logger as logger


class HttpCache:
    def __init__(self, session, browser):
        self.session = session
        self.browser = browser
        self.throttle_lock = {}
        self.rate_lock = {}

    def _log_path(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/logs/'

    def _site(self, url):
        words = re.findall('\w{3,}', url)
        return next(w for w in words if w not in ('https', 'http', 'www', 'dns', 'api'))

    def _cache(self, cache_days, fetch, url, params=None):
        url_params = url if not params else url + '?' + urllib.urlencode(params)
        url_hash = hashlib.sha1(url_params).hexdigest()
        site = self._site(url)
        filename = self._log_path() + '{}-{}.json'.format(site, url_hash)

        # reverse proxy (web accel)
        if os.path.isfile(filename):
            modified = datetime.fromtimestamp(os.path.getmtime(filename))
            invalidation_time = modified + timedelta(days=cache_days)
            if datetime.now() < invalidation_time:
                with codecs.open(filename, 'r', 'utf-8') as file:
                    logger.info('cached', *self._short_name(filename).split('-'))
                    return json.load(file)

        # rate lock
        if self.rate_lock.get(site):
            return None

        # avoid throttling
        if self.throttle_lock.get(site) and 'api.brewerydb' not in url:
            total_lock_time = (datetime.utcnow() - self.throttle_lock.pop(site)).total_seconds()
            delay = timedelta(seconds=3 + randint(0, 7)).total_seconds()
            logger.info('delay', 'wait for ' + str(delay) + 's')
            time.sleep(max(delay - total_lock_time, 0))

        # request
        self.throttle_lock[site] = datetime.utcnow()
        result = fetch()

        # local store
        with codecs.open(filename, 'w', 'utf-8') as file:
            logger.warn('get', *self._short_name(filename).split('-'))
            file.truncate()
            file.write(unicode(json.dumps(result, indent=2, ensure_ascii=False)))

        return result

    @staticmethod
    def _short_name(filename):
        return re.findall(r'(?<=\/)\w{3,}\-\w{3,}(?=\.json)', filename)[0]

    def get(self, cache_days, url, params=None, map_to=lambda r: r.json()):
        def fetch():
            response = self.session.get(url, params=params)
            response.raise_for_status()
            if int(response.headers.get('X-Ratelimit-Remaining', 101)) < 10:
                self.rate_lock[self._site(url)] = True
                logger.err('rate-limit', 'restricting access')
            return map_to(response)
        return self._cache(cache_days, fetch, url, params=params)

    def visit(self, cache_days, url, map_to=None):
        def fetch():
            self.browser.visit(url)
            return map_to(self.browser)
        return self._cache(cache_days, fetch, url)

    def robot_allowed(self, url, url_robot):
        robots_text = self.get(3, url_robot, map_to=lambda r: r.text)
        rp = robotparser.RobotFileParser()
        rp.parse(robots_text)
        if not rp.can_fetch('*', url):
            raise ValueError('Robot is not allowed to fetch {}'.format(url))
