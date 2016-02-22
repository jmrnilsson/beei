from utils import url_sb


def find_all_by_page(session, page):
    return session.get(30, url_sb().format(page=page))
