import sys


class __colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _print(colour, command, message, hash):
    msg = (colour + command + ': ').ljust(20, ' ') + __colors.ENDC
    if hash:
        msg += unicode(message).ljust(25) + unicode(hash)
    else:
        msg += unicode(message)
    print >> sys.stdout, msg


def info(command, message, hash=None):
    _print(__colors.OKGREEN, command, message, hash)


def warn(command, message, hash=None):
    _print(__colors.WARNING, command, message, hash)


def err(command, message):
    _print(__colors.FAIL, command, message, None)


def warning(*args, **kwargs):
    return warn(*args, **kwargs)


def information(*args, **kwargs):
    return info(*args, **kwargs)


def error(*args, **kwargs):
    return err(*args, **kwargs)


def _logo():
    return r'''
                    ___           ___
     _____         /  /\         /  /\        ___
    /  /::\       /  /:/_       /  /:/_      /  /\
   /  /:/\:\     /  /:/ /\     /  /:/ /\    /  /:/
  /  /:/~/::\   /  /:/ /:/_   /  /:/ /:/_  /__/::\
 /__/:/ /:/\:| /__/:/ /:/ /\ /__/:/ /:/ /\ \__\/\:\__
 \  \:\/:/~/:/ \  \:\/:/ /:/ \  \:\/:/ /:/    \  \:\/\
  \  \::/ /:/   \  \::/ /:/   \  \::/ /:/      \__\::/
   \  \:\/:/     \  \:\/:/     \  \:\/:/       /__/:/
    \  \::/       \  \::/       \  \::/        \__\/
     \__\/         \__\/         \__\/

'''


print >> sys.stdout, __colors.OKBLUE + _logo() + __colors.ENDC
