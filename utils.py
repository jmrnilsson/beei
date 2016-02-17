import os
# import inspect
import json
# import bee


def json_load_config(name):
    # path = os.path.dirname(os.path.abspath(inspect.getfile(bee)))
    path = os.path.dirname(os.path.abspath(__file__))
    response_file = os.path.dirname(path + '/config/') + '/' + name
    with open(response_file) as response:
        return json.load(response)


def url_sb():
    return json_load_config('config.json')['url_sb']


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
