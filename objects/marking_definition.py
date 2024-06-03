import json
from stix2 import parse
from helpers import utils

def make_disarm_marking_definition(identity_id=None):

    DEFAULT_OBJECT_URL = [
        "https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/marking-definition/disarm2stix.json",
    ]
    object_list = []
    for obj in DEFAULT_OBJECT_URL:
        object = parse(json.loads(utils.load_file_from_url(obj)))
        if not utils.fs.get(object.get("id")):
            utils.fs.add(object)
        object_list.append(json.loads(utils.load_file_from_url(obj)))
    return object_list


def custom_md():
    return ["marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487"
            ]+[make_disarm_marking_definition()[0].get("id")]
