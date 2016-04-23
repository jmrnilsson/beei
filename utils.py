import os
import sys
import json


def json_load_config(name):
    filename = os.path.dirname(os.path.abspath(__file__)) + '/' + name
    with open(filename) as file:
        return json.load(file)


def _print_line(colour, command, message, hash):
    msg = (colour + command + ': ').ljust(14, ' ') + _colors.ENDC
    if hash:
        msg += unicode(message).ljust(50) + unicode(hash)
    else:
        msg += unicode(message)
    print >> sys.stdout, msg


def info(command, message, hash=None):
    _print_line(_colors.OKGREEN, command, message, hash)


def warn(command, message, hash=None):
    _print_line(_colors.WARNING, command, message, hash)


def err(command, message):
    _print_line(_colors.FAIL, command, message)


class _colors:
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
