from collections import OrderedDict
from stix2 import CustomObject, properties, ExternalReference
from stix2.v21.common import _STIXBase21
from datetime import datetime
import uuid
from uuid import UUID
from helpers import utils

class MitreContent(_STIXBase21):
    """
    
    """
    _properties = OrderedDict([
        ('object_modified', properties.TimestampProperty()),
        ('object_ref', properties.ReferenceProperty(invalid_types=[], required=True))
    ])

@CustomObject('x-mitre-collection', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('x_mitre_contents', properties.ListProperty(MitreContent, required=True)),
])
class Collection:
    pass

def make_disarm_collection(objects, identity_id, marking_id, date):
    name = 'DISARM Red Framework'
    description = 'Incident creator TTPs.'
    # tactic_refs = [i.id for i in tactics]
    mitre_collection = Collection(
        id=f"x-mitre-collection--{uuid.uuid5(namespace=UUID('8700e156-6ce9-5090-8589-f9d0aef7bdb7'), name='DISARM Red Framework')}",
        name=name,
        description=description,
        external_references=[
            {
                "source_name": "DISARM",
                "url": "https://www.disarm.foundation/",
                "external_id": "DISARM"
            }
        ],
        x_mitre_contents=[dict(object_ref=obj['id'], object_modified=obj.get('modified')) for obj in objects],
        allow_custom=True,
        object_marking_refs=marking_id,
        created_by_ref = identity_id,
        created="2020-01-01T00:00:00.000Z",
        modified=datetime.strptime(date, '%Y-%m-%d'),
    )
    utils.fs.add(mitre_collection)
    return [mitre_collection]