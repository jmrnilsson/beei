import http_cache
from utils import url_sb


def find_all_by_page(page):
    return http_cache.get(url_sb().format(page=page), hint='sb', cache_days=30)
