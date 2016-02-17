from datetime import datetime
import re
from http_cache import HttpCache
from utils import url_invalid_ip_address, url_check_ip


def check():
    def map_ip(response):
        ip = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response.text)
        return {
            'ip': ip[0],
            'utc_datetime': str(datetime.utcnow())
        }

    return HttpCache(0, to_dict=map_ip).get(url_check_ip())['ip']


def find_all_void():
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

    return HttpCache(150, to_dict=map_ip_ranges).get(url_invalid_ip_address())


def ok():
    def zfill(ip_address):
        return '.'.join([number.zfill(3) for number in ip_address.split('.')])

    ip = check()
    ip_zfill = zfill(ip)
    for ip_range in find_all_void():
        if zfill(ip_range['start']) < ip_zfill < zfill(ip_range['end']):
            raise RuntimeError('Found ip ({}) in {}'.format(ip, ip_range['owner']))
