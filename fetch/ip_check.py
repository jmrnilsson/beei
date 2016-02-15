from datetime import datetime
import re
import http_cache
from utils import url_invalid_ip_address, url_check_ip


def check_ip():
    def map_ip(html_source):
        ip = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', html_source)
        return {'ip': _zfill(ip[0])}

    json_ip = http_cache.get(url_check_ip(), hint='checkip', to_json=map_ip)
    return json_ip


def find_all_invalid_ip_addresses():
    def map_ip_ranges(text):
        return [to_ip_range(l) for l in text.splitlines() if len(l) > 10]

    def to_ip_range(line):
        properties = line.split(',')
        assigned = datetime.strptime(properties[3], '%d/%m/%y')

        return {
            'start': _zfill(properties[0]),
            'end': _zfill(properties[1]),
            'assigned': datetime.strftime(assigned, '%Y-%m-%d'),
            'owner': properties[4]
        }

    return http_cache.get(url_invalid_ip_address(),
                          cache_days=50,
                          hint='ip',
                          to_json=map_ip_ranges)


def _zfill(ip):
    return '.'.join([number.zfill(3) for number in ip.split('.')])
