import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def handle_bson(value):
    if type(value) == list:
        for item in value:
            item['_id'] = str(item.get('_id'))
    elif type(value) == dict:
        value['_id'] = str(value.get('_id'))
    return value
