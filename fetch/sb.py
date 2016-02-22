import robotparser
from http_cache import HttpCache
from utils import sb_url, sb_url_robots, sb_next_page


def find_all_by_page(page):
    url = sb_url().format(page=page).encode('utf-8')
    _robot_can_fetch(url)
    response = HttpCache(30).get(url)
    next_page_selector0, next_page_selector1 = sb_next_page()
    return response, response[next_page_selector0][next_page_selector1]


def _robot_can_fetch(url):
    robots_text = HttpCache(5, map_to=lambda r: r.text).get(sb_url_robots())
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))

