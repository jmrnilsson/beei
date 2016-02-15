import requests
import hashlib
import urllib
import json
import os.path
import inspect
from datetime import datetime, timedelta
import bee

def get(url, params=None, hint=None, cache_days=0, to_json=None):
    url_params = url if not params else url + '?' + urllib.urlencode(params)
    hash = hashlib.sha1(url_params).hexdigest()
    filename = '{}-{}'.format(hint, hash) if hint else hash
    path = os.path.dirname(os.path.abspath(inspect.getfile(bee)))
    filename = path + '/logs/' + filename + '.json'

    if os.path.isfile(filename):
        modified = datetime.fromtimestamp(os.path.getmtime(filename))
        renewal = modified + timedelta(days=cache_days)
        if datetime.now() < renewal:
            with open(filename, 'r') as storage:
                return json.load(storage)

    response = requests.get(url, params=params)
    with open(filename, 'w') as storage:
        storage.truncate()
        json_content = to_json(response.text) if to_json else response.json()
        storage.write(json.dumps(json_content, indent=2))

    return json_content
