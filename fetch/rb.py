import zipfile
import StringIO
from utils.config import RB_URL_ROBOTS, RB_URL


def _download_zip(session):
    def map_to(r):
        output = StringIO.StringIO()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                output.write(chunk)
                # output.flush()
        zip = zipfile.ZipFile(output)
        # for name in zip.namelist():
        content = zip.read('beers.txt').decode('utf16')
        lines = content.splitlines()
        headers = ['name', 'brewer', 'rate', 'thing']
        rows = []
        for line in lines:
            _, name, _, brewer, rate, thing = line.split('\t')[:6]
            rows.append([name, brewer, rate])
        return {'headers': headers, 'rows': rows}

    session.robot_allowed(RB_URL, RB_URL_ROBOTS)
    return session.get_streamed(14, RB_URL, map_to=map_to)


def get_all(http):
    beers = _download_zip(http)
    return [dict(zip(beers.get('headers'), b)) for b in beers.get('rows')]
