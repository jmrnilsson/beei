import os
import json


def json_load_config(name):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.dirname(path + '/config/') + '/' + name
    with open(filename) as file:
        return json.load(file)


def sb_url():
    return json_load_config('config.json')['url_sb']


def sb_url_robots():
    return json_load_config('config.json')['url_sb_robots']


def sb_name_0():
    return json_load_config('config.json')['sb_name_0']


def sb_list():
    return json_load_config('config.json')['sb_list']


def sb_name_1():
    return json_load_config('config.json')['sb_name_1']


def url_invalid_ip_address():
    return json_load_config('config.json')['url_invalid_ip']


def url_check_ip():
    return json_load_config('config.json')['url_check_ip']


def brewery_db_api_key():
    return json_load_config('config.json')['brewery_db_api_key']
