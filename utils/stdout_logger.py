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
    msg = (colour + command + ': ').ljust(14, ' ') + __colors.ENDC
    if hash:
        msg += unicode(message).ljust(50) + unicode(hash)
    else:
        msg += unicode(message)
    print >> sys.stdout, msg


def info(command, message, hash=None):
    _print(__colors.OKGREEN, command, message, hash)


def warn(command, message, hash=None):
    _print(__colors.WARNING, command, message, hash)


def err(command, message):
    _print(__colors.FAIL, command, message)


def warning(*args, **kwargs):
    return warn(*args, **kwargs)


def information(*args, **kwargs):
    return info(*args, **kwargs)


def error(*args, **kwargs):
    return err(*args, **kwargs)
