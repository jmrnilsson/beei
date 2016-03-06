import robotparser
from utils import config
from splinter import Browser


def index(session):
    url = config.rb_url()
    _robot_can_fetch(session, url)

    def fetch():
        with Browser(**config.browser_kwargs()) as browser:
            browser.visit(url)
            styles = []
            group_names = browser.find_by_xpath("//*[contains(@class, 'groupname')]")
            for group_name in group_names:
                elements = group_name.find_by_xpath('following-sibling::ul[1]/li/a')
                for el in elements:
                    styles.append({'group': group_name.text, 'name': el.text, 'href': el['href']})

        return styles

    session.visit(3, url, fetch)


def _robot_can_fetch(session, url):
    robots_text = session.get(5, config.rb_robots(), map_to=lambda r: r.text)
    rp = robotparser.RobotFileParser()
    rp.parse(robots_text)
    if not rp.can_fetch('*', url):
        raise ValueError('Robot is not allowed to fetch {}'.format(url))
