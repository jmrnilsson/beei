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
            group_names = browser.find_by_css('.groupname')
            for group_name in group_names:
                group = None
                xpath_expression = "../ul/li/a | ../*[contains(@class, 'groupname')]"
                elements = group_name.find_by_xpath(xpath_expression)
                for el in elements:
                    if el.tag_name == 'a':
                        styles.append({'group': group, 'name': el.text, 'href': el['href']})
                    else:
                        group = el.text

        return styles

    session.visit(0, url, fetch)


def _robot_can_fetch(session, url):
    robots_text = session.get(5, config.rb_robots(), map_to=lambda r: r.text)
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))
