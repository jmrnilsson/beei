import os
import json
import re
import codecs
from utils import stdout_logger as logger


class BeerList:
    def __init__(self):
        self.__items = []
        self.__attrs = ('abv', 'alcohol', 'name', '^volume$', '^price$', 'sellstart',
                        'score', 'url', 'href', '^type$')

    def add(self, b):
        if not b or len(b.keys()) < 0:
            return

        self.__items.append({
            k: v for k, v in b.iteritems()
            if any([a for a in self.__attrs if any(re.findall(a, k.lower()))])
        })

    def save(self):
        filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/beers.json'
        with codecs.open(filename, 'w', 'utf-8') as file:
            logger.info('write', 'to ' + filename)
            file.truncate()
            file.write(unicode(json.dumps(self.__items, indent=2, ensure_ascii=False)))