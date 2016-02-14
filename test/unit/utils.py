import os
import inspect
import json
import beei


def get_logged_response(name):
    path = os.path.dirname(os.path.abspath(inspect.getfile(beei)))
    response_file = os.path.dirname(path + '/logs/') + '/' + name
    with open(response_file) as response:
        return json.load(response)
