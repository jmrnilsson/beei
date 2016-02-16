from http_cache import HttpCache
from utils import url_sb


def find_all_by_page(page):
    return HttpCache(30).get(url_sb().format(page=page))
