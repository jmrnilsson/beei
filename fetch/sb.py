import requests
from utils import sb_url


def find_all_by_page(page):
    url = sb_url().format(page=page)
    response = requests.get(url)
    return response.json()

