import robotparser
from utils import config


def find_all_by_page(session, page):
    url = config.sb_url().format(page=page).encode('utf-8')
    _robot_can_fetch(session, url)
    response = session.get(30, url)
    next_page_selector0, next_page_selector1 = config.sb_next_page()
    return response, response[next_page_selector0][next_page_selector1]


def _robot_can_fetch(session, url):
    robots_text = session.get(5, config.sb_robots(), map_to=lambda r: r.text)
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))
