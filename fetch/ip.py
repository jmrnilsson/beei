import sys
from datetime import datetime
import re
from utils import url_invalid_ip_address, url_check_ip


class IP:
    def __init__(self, session):
        self.session = session

    def ok(self):
        return _ok(self.session)

    def check(self):
        return _ok(self.session)


def _check(session):
    def map_ip(response):
        ip = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response.text)[0]
        print >> sys.stdout, 'ip: ' + unicode(ip)
        return {
            'ip': ip,
            'utc_datetime': str(datetime.utcnow())
        }

    return session.get(url_check_ip(), 0, map_to=map_ip)
    # return HttpCache(0, map_to=map_ip).get(url_check_ip())['ip']


def _find_all_void(session):
    def map_ip_ranges(response):
        return [to_ip_range(l) for l in response.text.splitlines() if len(l) > 10]

    def to_ip_range(line):
        start, end, _, assigned, owner = line.split(',')[:5]
        assigned = datetime.strptime(assigned, '%d/%m/%y')
        assigned = datetime.strftime(assigned, '%Y-%m-%d')
        return {
            'start': start,
            'end': end,
            'assigned': assigned,
            'owner': owner
        }

    return session.get(url_invalid_ip_address(), 150, map_to=map_ip_ranges)
    # return HttpCache(150, map_to=map_ip_ranges).get(url_invalid_ip_address())


def _ok(session):
    def zfill(ip_address):
        return '.'.join([number.zfill(3) for number in ip_address.split('.')])

    ip = _check(session)
    ip_zfill = zfill(ip)
    for ip_range in _find_all_void(session):
        if zfill(ip_range['start']) < ip_zfill < zfill(ip_range['end']):
            raise RuntimeError('Found ip ({}) in {}'.format(ip, ip_range['owner']))

    return True
