import robotparser
from http_cache import HttpCache
from utils import sb_url, sb_url_robots


def find_all_by_page(page):
    url = sb_url().format(page=page)
    _robot_can_fetch(url)
    return HttpCache(30).get(url)


def _robot_can_fetch(url):
    robots_text = HttpCache(5, map_to=lambda r: r.text).get(sb_url_robots())
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url.encode('utf-8')):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))

