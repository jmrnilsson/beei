from datetime import datetime
import re
import http_cache
from utils import url_invalid_ip_address, url_check_ip


def check_ip():
    def map_ip(html_source):
        ip = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', html_source)
        return {
            'ip': ip[0],
            'utc_datetime': str(datetime.utcnow())
        }

    return http_cache.get(url_check_ip(), hint='check_ip', to_json=map_ip)


def find_all_invalid_ip_addresses():
    def map_ip_ranges(text):
        return [to_ip_range(l) for l in text.splitlines() if len(l) > 10]

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

    url = url_invalid_ip_address()
    return http_cache.get(url, cache_days=50, hint='ip_list', to_json=map_ip_ranges)


def assert_ok_ip():
    def zfill(ip_address):
        return '.'.join([number.zfill(3) for number in ip_address.split('.')])

    ip = check_ip()['ip']
    ip_zfill = zfill(ip)
    for ip_range in find_all_invalid_ip_addresses():
        if zfill(ip_range['start']) < ip_zfill < zfill(ip_range['end']):
            raise RuntimeError('Using a void ip {} in range {}'.format(ip, ip_range['owner']))
