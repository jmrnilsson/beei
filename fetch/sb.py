from utils.config import SB_URL, SB_URL_ROBOTS, SB_SELECTORS_NEXT_PAGE


def find_all_by_page(session, page):
    url = SB_URL.format(page=page).encode('utf-8')
    session.robot_allowed(url, SB_URL_ROBOTS)
    response = session.get(30, url)
    sel_0, sel_1 = SB_SELECTORS_NEXT_PAGE
    return response, response[sel_0][sel_1]
