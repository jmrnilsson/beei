from xml.etree import ElementTree
import utils.stdout_logger as logger
from utils.config import SB_URL, SB_URL_ROBOTS, SB_SELECTORS_NEXT_PAGE, SB_URL_SITE_MAP


def index_api_by_page(session, page):
    url = SB_URL.format(page=page).encode('utf-8')
    session.robot_allowed(url, SB_URL_ROBOTS)
    response = session.get(30, url)
    sel_0, sel_1 = SB_SELECTORS_NEXT_PAGE
    return response, response[sel_0][sel_1]


def index_site_map(session):
    def map_to(r):
        root = ElementTree.fromstring(r.content)
        res = []
        for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            res.append(loc.text)
        logger.info('site_map', str(res))
        return res

    session.robot_allowed(SB_URL_SITE_MAP, SB_URL_ROBOTS)
    return session.get(0, SB_URL_SITE_MAP, map_to=map_to)
