from xml.etree import ElementTree
import re
from utils.config import SB_URL, SB_URL_ROBOTS, SB_SELECTORS_NEXT_PAGE, SB_URL_SITE_MAP

__ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


def index_api_by_page(session, page):
    url = SB_URL.format(page=page).encode('utf-8')
    session.robot_allowed(url, SB_URL_ROBOTS)
    response = session.get(30, url)
    sel_0, sel_1 = SB_SELECTORS_NEXT_PAGE
    return response, response[sel_0][sel_1]


def index_site_map(session):
    def map_to(r):
        root = ElementTree.fromstring(r.content)
        return [loc.text for loc in root.findall('.//sitemap:loc', __ns)]

    session.robot_allowed(SB_URL_SITE_MAP, SB_URL_ROBOTS)
    return session.get(10, SB_URL_SITE_MAP, map_to=map_to)


def get_by_site_map(session, url):
    def map_to(r):
        root = ElementTree.fromstring(r.content)
        return [
            loc.text for loc in root.findall('.//sitemap:loc', __ns)
            if any(re.findall(r'.*\.se\/dryck\/ol\/', loc.text))
        ]

    session.robot_allowed(url, SB_URL_ROBOTS)
    return session.get(10, url, map_to=map_to)


'''
stream
def get_by_site_map(session, url):
    def map_to(r):
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        events = ElementTree.iterparse(response.raw)
        for elem, event in events:


    session.robot_allowed(url, SB_URL_ROBOTS)
    return session.get(1, url, map_to=map_to)
'''
