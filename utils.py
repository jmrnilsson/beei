import os
import sys
import json


def json_load_config(name):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.dirname(path + '/config/') + '/' + name
    with open(filename) as file:
        return json.load(file)


def print_line(colour, command, msg):
    print >> sys.stdout, (colour + command + ': ').ljust(14, ' ') + BColours.ENDC + unicode(msg)


class BColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Config(object):
    def __init__(self):
        self.config = json_load_config('config.json')

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
