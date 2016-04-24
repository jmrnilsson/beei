from utils.config import RB_URL_ROBOTS, RB_URL


def index(session):
    def map_to(browser):
        styles = []
        group_names = browser.find_by_xpath("//*[contains(@class, 'groupname')]")
        for group_name in group_names:
            elements = group_name.find_by_xpath('following-sibling::ul[1]/li/a')
            for el in elements:
                styles.append({'group': group_name.text, 'name': el.text, 'href': el['href']})
        return styles

    url = RB_URL
    session.robot_allowed(url, RB_URL_ROBOTS)
    return session.visit(3, url, map_to=map_to)


def get_top_50_for_style(session, url):
    def map_to(browser):
        headers = []
        top_50 = []
        rows = browser.find_by_css('#styleList > table.table > tbody > tr')
        for header in rows[0].find_by_css('th')[1:]:
            headers.append(header.text.lower())
        for index, row in enumerate(rows[1:]):
            beer = {}
            for index, attr in enumerate(row.find_by_css('td')[1:]):
                if index == 0:
                    link = attr.find_by_css('a')
                    beer.update({'href': link['href'], headers[index]: link.text})
                else:
                    beer[headers[index]] = attr.text
            top_50.append(beer)
        return top_50

    session.robot_allowed(url, RB_URL_ROBOTS)
    return session.visit(15, url, map_to=map_to)
