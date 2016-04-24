import os
import json


def __load():
    filename = os.path.dirname(os.path.abspath(__file__)) + '/../config.json'
    with open(filename) as file:
        return json.load(file)

__config = __load()

SB_URL = __config['sb_url']
SB_URL_ROBOTS = __config['sb_robots']
SB_URL_SITE_MAP = __config['sb_url_site_map']
SB_SELECTOR_LIST = __config['sb_list']
SB_SELECTORS_NEXT_PAGE = __config['sb_next_page'].split('.')
SB_SELECTORS_NAME = __config['sb_name'].split(';')

IP_URL_LIST_BLOCKED = __config['ip_url_void_list']
IP_URL_CHECK = __config['ip_url_check']

BREWERY_DB_API_KEY = __config['brewery_db_api_key']

RB_URL = __config['rb_url']
RB_URL_ROBOTS = __config['rb_robots']

BROWSER_KWARGS = __config['browser_kwargs']
