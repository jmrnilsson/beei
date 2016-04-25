from datetime import datetime
import re
from utils import stdout_logger as logger
from utils.config import IP_URL_CHECK, IP_URL_LIST_BLOCKED


def _get_ip(session):
    def map_ip(response):
        ip = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', response.text)[0]
        logger.info('ip', ip)
        return {
            'ip': ip,
            'utc_datetime': unicode(datetime.utcnow())
        }
    return session.get(0, IP_URL_CHECK, map_to=map_ip)


def _get_blocked_ip(session):
    def map_ip_ranges(response):
        def to_ip_range(line):
            start, end, _, assigned, owner = line.split(',')[:5]
            return {
                'start': start,
                'end': end,
                'assigned': datetime.strptime(assigned, '%d/%m/%y').strftime('%Y-%m-%d'),
                'owner': owner
            }
        return [to_ip_range(l) for l in response.text.splitlines() if len(l) > 10]
    return session.get(1, IP_URL_LIST_BLOCKED, map_to=map_ip_ranges)


def _zfill(ip_address):
    return '.'.join([number.zfill(3) for number in ip_address.split('.')])


def ok(session):
    ip = _get_ip(session)['ip']
    zfill_ip = _zfill(ip)
    for ip_range in _get_blocked_ip(session):
        if _zfill(ip_range['start']) < zfill_ip < _zfill(ip_range['end']):
            raise RuntimeError('Found ip ({}) in {}'.format(ip, ip_range['owner']))
    return True
