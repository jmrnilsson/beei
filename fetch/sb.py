import robotparser
from utils.config import SB_URL, SB_URL_ROBOTS, SB_SELECTORS_NEXT_PAGE


def find_all_by_page(session, page):
    url = SB_URL.format(page=page).encode('utf-8')
    _robot_allowed(session, url)
    response = session.get(30, url)
    sel_0, sel_1 = SB_SELECTORS_NEXT_PAGE
    return response, response[sel_0][sel_1]


def _robot_allowed(session, url):
    robots_text = session.get(5, SB_URL_ROBOTS, map_to=lambda r: r.text)
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))
