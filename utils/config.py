import os
import json


def __load():
    filename = os.path.dirname(os.path.abspath(__file__)) + '/../config.json'
    with open(filename) as file:
        return json.load(file)

__config = __load()

SB_URL = __config['sb_url']
SB_URL_ROBOTS = __config['sb_robots']
SB_SELECTOR_LIST = __config['sb_list']
SB_SELECTORS_NEXT_PAGE = __config['sb_next_page'].split('.')
SB_SELECTORS_NAME = __config['sb_name'].split(';')

IP_URL_LIST_BLOCKED = __config['ip_url_void_list']
IP_URL_CHECK = __config['ip_url_check']

BREWERY_DB_API_KEY = __config['brewery_db_api_key']

RB_URL = __config['rb_url']
RB_URL_ROBOTS = __config['rb_robots']

BROWSER_KWARGS = __config['browser_kwargs']

'''
class Config(object):
    def __init__(self):
        filename = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        with open(filename) as file:
            self.config = json.load(file)

    def sb_url(self):
        return self.config['sb_url']

    def sb_robots(self):
        return self.config['sb_robots']

    def sb_list(self):
        return self.config['sb_list']

    def sb_next_page(self):
        return self.config['sb_next_page'].split('.')

    def sb_name_0(self):
        return self.config['sb_name_0']

    def sb_name_1(self):
        return self.config['sb_name_1']

    def ip_url_void_list(self):
        return self.config['ip_url_void_list']

    def ip_url_check(self):
        return self.config['ip_url_check']

    def brewery_db_api_key(self):
        return self.config['brewery_db_api_key']

    def rb_url(self):
        return self.config['rb_url']

    def rb_robots(self):
        return self.config['rb_robots']

    def browser_kwargs(self):
        return self.config['browser_kwargs']


config = Config()
'''
