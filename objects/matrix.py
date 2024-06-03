from stix2 import CustomObject, properties, ExternalReference
from datetime import datetime
import uuid
from uuid import UUID
from helpers import utils


@CustomObject('x-mitre-matrix', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('tactic_refs', properties.ListProperty(properties.ReferenceProperty(valid_types="SDO"), required=True))
])
class Matrix(object):
    def __init__(self, **kwargs):
        if True:
            pass

def make_disarm_matrix(tactics, identity_id, marking_id, date):
    name = 'DISARM Red Framework'
    description = 'Incident creator TTPs.'
    tactic_refs = [i.id for i in tactics]
    matrix = Matrix(
        id=f"x-mitre-matrix--{uuid.uuid5(namespace=UUID('8700e156-6ce9-5090-8589-f9d0aef7bdb7'), name='DISARM Red Framework')}",
        name=name,
        description=description,
        external_references=[
            {
                "source_name": "DISARM",
                "url": "https://www.disarm.foundation/",
                "external_id": "DISARM"
            }
        ],
        tactic_refs=tactic_refs,
        allow_custom=True,
        object_marking_refs=marking_id,
        created_by_ref = identity_id,
        created="2020-01-01T00:00:00.000Z",
        modified=datetime.strptime(date, '%Y-%m-%d'),
    )
    utils.fs.add(matrix)
    return [matrix]