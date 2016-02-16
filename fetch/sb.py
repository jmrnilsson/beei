from http_cache import HttpCache
from utils import url_sb


def find_all_by_page(page):
    http_cache = HttpCache(30)
    return http_cache.get(url_sb().format(page=page))
