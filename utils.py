import os
import sys
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


def sb_next_page():
    return json_load_config('config.json')['sb_next_page'].split('.')


def sb_name_1():
    return json_load_config('config.json')['sb_name_1']


def url_invalid_ip_address():
    return json_load_config('config.json')['url_invalid_ip']


def url_check_ip():
    return json_load_config('config.json')['url_check_ip']


def brewery_db_api_key():
    return json_load_config('config.json')['brewery_db_api_key']


class BColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_line(colour, command, msg):
    print >> sys.stdout, (colour + command + ': ').ljust(14, ' ') + BColours.ENDC + unicode(msg)