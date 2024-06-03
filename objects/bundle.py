from stix2 import Bundle
import uuid
import json
from uuid import UUID
from helpers import file, utils
import hashlib

def generate_md5_from_list(stix_objects: list) -> str:

    json_str = json.dumps(stix_objects, sort_keys=True).encode('utf-8')
    return hashlib.md5(json_str).hexdigest()

def serialized_json(stix_objects):
    temp_object_list = []
    for obj in iter(stix_objects):
        if not isinstance(obj, dict):
            temp_object_list.append(obj.serialize())
        else:
            temp_object_list.append(obj)
    return temp_object_list

def make_stix_bundle(stix_objects):
    id = "bundle--{}".format(
        uuid.uuid5(
            namespace=UUID('8700e156-6ce9-5090-8589-f9d0aef7bdb7'),
            name=generate_md5_from_list(stix_objects=serialized_json(stix_objects))
        )
    )
    bundle = Bundle(
        id=id,
        objects=stix_objects, allow_custom=True)

    timestamp_filename = utils.publish_datetime_format(str(stix_objects[0].get("created")).split(" ")[0])
    file.write_json_file(
        f"stix2_objects/bundle/{id}/",
        f"{timestamp_filename}.json",
        json.loads(bundle.serialize()),
    )
    file.write_json_file(
        f"stix2_objects/",
        f"disarm-bundle.json",
        json.loads(bundle.serialize()),
    )
    return bundle