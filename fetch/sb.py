import requests
from utils import url_sb


def find_all_by_page(page):
    return requests.get(url_sb().format(page=page)).json()
