import robotparser
from utils import config
from splinter import Browser
# http://stackoverflow.com/questions/17380869/get-list-items-inside-div-tag-using-xpath


def index(session):
    url = config.rb_url()
    _robot_can_fetch(session, url)

    def fetch():
        with Browser(**config.browser_kwargs()) as browser:
            browser.visit(url)
            styles = []
            group_expr = "//*[contains(@class, 'groupname')]"
            group_names = browser.find_by_xpath(group_expr)
            for group_name in group_names:
                style_group_expr = "following-sibling::ul[1]/li/a"
                elements = group_name.find_by_xpath(style_group_expr)
                for el in elements:
                    styles.append({'group': group_name.text, 'name': el.text, 'href': el['href']})

        return styles

    session.visit(0, url, fetch)


def _robot_can_fetch(session, url):
    robots_text = session.get(5, config.rb_robots(), map_to=lambda r: r.text)
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))
