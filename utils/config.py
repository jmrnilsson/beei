import os
import json


def __load():
    filename = os.path.dirname(os.path.abspath(__file__)) + '/../config.json'
    with open(filename) as file:
        return json.load(file)

__config = __load()

BREWERY_DB_API_KEY = __config['brewery_db_api_key']

IP_URL_BLOCKED = __config['ip_url_blocked']
IP_URL_CHECK = __config['ip_url_check']

RB_URL = __config['rb_url']
RB_URL_ROBOTS = __config['rb_robots']

SYS_URL = __config['sys_url']
SYS_URL_ROBOTS = __config['sys_robots']
SYS_TRANSLATIONS = __config['sys_translations']

BROWSER_KWARGS = __config['browser_kwargs']
USER_AGENT = __config['browser_kwargs']['user_agent']
