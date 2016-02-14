import requests
from utils import sb_url


def find_all_by_page(page):
    return requests.get(sb_url().format(page=page)).json()
