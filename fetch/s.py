from xml.etree import ElementTree
from utils.config import S_URL_ROBOTS, S_URL_API, S_API_MAP as map


def api_get_all(session):
    def map_to(r):
        root = ElementTree.fromstring(r.content)
        return [
            {
                k: article.find(v).text for k, v in map.iteritems()
                if article.find(v) is not None
            } for article in root.findall('.//artikel')
            if all(
                [
                    article.find(map['category']) is not None,
                    u'\xd6l' in article.find(map['category']).text
                ]
            )
        ]

    session.robot_allowed(S_URL_API, S_URL_ROBOTS)
    return session.get(10, S_URL_API, map_to=map_to)
