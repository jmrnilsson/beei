import os
import inspect
import json
import bee


def json_load_config(name):
    path = os.path.dirname(os.path.abspath(inspect.getfile(bee)))
    response_file = os.path.dirname(path + '/config/') + '/' + name
    with open(response_file) as response:
        return json.load(response)


def sb_url():
    return json_load_config('config.json')['sb_url']


def brewery_db_api_key():
    return json_load_config('config.json')['brewery_db_api_key']
