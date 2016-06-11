from xml.etree import ElementTree
from utils.config import SYS_URL_ROBOTS, SYS_URL, SYS_TRANSLATIONS as translations


def get_all(session):
    def map_to(response):
        root = ElementTree.fromstring(response.content)
        return [
            {
                k: article.find(v).text for k, v in map.iteritems()
                if article.find(v) is not None
            } for article in root.findall('.//artikel')
            if all(
                [
                    article.find(translations['category']) is not None,
                    u'\xd6l' in article.find(translations['category']).text
                ]
            )
        ]

    session.robot_allowed(SYS_URL, SYS_URL_ROBOTS)
    return session.get(10, SYS_URL, map_to=map_to)
