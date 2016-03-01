from datetime import datetime
import re
from utils import config, BColours, print_line


def check(session):
    def map_ip(response):
        ip = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response.text)[0]
        print_line(BColours.OKGREEN, 'ip', ip)
        return {
            'ip': ip,
            'utc_datetime': str(datetime.utcnow())
        }

    return session.get(0, config.ip_url_check(), map_to=map_ip)


def _find_all_void(session):
    def map_ip_ranges(response):
        return [to_ip_range(l) for l in response.text.splitlines() if len(l) > 10]

    def to_ip_range(line):
        start, end, _, assigned, owner = line.split(',')[:5]
        return {
            'start': start,
            'end': end,
            'assigned': datetime.strptime(assigned, '%d/%m/%y').strftime('%Y-%m-%d'),
            'owner': owner
        }

    return session.get(1, config.ip_url_void_list(), map_to=map_ip_ranges)


def ok(session):
    def zfill(ip_address):
        return '.'.join([number.zfill(3) for number in ip_address.split('.')])

    ip = check(session)['ip']
    ip_zfill = zfill(ip)
    for ip_range in _find_all_void(session):
        if zfill(ip_range['start']) < ip_zfill < zfill(ip_range['end']):
            raise RuntimeError('Found ip ({}) in {}'.format(ip, ip_range['owner']))

    return True
