import uuid
from stix2 import CustomObject, properties, ExternalReference
from uuid import UUID
from helpers import utils
from datetime import datetime

import objects.marking_definition
from objects import identity, marking_definition

valid_tactics = [
        "plan-strategy", #TA01
        "plan-objectives", #TA02
        "microtarget", #TA05
        "develop-content", #TA06
        "select-channels-and-affordances", #TA07
        "conduct-pump-priming", #TA08
        "deliver-content", #TA09
        "drive-offline-activity", #TA010
        "persist-in-the-information-environment", #TA11
        "assess-effectiveness", #TA12
        "target-audience-analysis", #TA13
        "develop-narratives", #TA14
        "establish-assets", #TA15
        "establish-legitimacy", #TA16
        "maximise-exposure", #TA17
        "drive-online-harms" #TA18
    ]

@CustomObject('x-mitre-tactic', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('x_mitre_shortname', properties.StringProperty(required=True)),
    ('external_references', properties.ListProperty(ExternalReference))
])
class Tactic(object):
    def __init__(self, x_mitre_shortname=None, **kwargs):
        if x_mitre_shortname and x_mitre_shortname not in valid_tactics:
            raise ValueError("'%s' is not a recognized DISARM Tactic." % x_mitre_shortname)

def make_disarm_tactics(data, identity_id, marking_id, date):
    tactics = []
    for t in data["tactics"].values.tolist():
        tactic = Tactic(
            id = "x-mitre-tactic--{}".format(uuid.uuid5(namespace=UUID("8700e156-6ce9-5090-8589-f9d0aef7bdb7"),name=f"{t[0]}")),
            name=f"{t[1]}",
            description=f"{t[5]}",
            x_mitre_shortname=f'{t[1].lower().replace(" ", "-")}',
            created="2020-01-01T00:00:00.000Z",
            modified=datetime.strptime(date, '%Y-%m-%d'),
            external_references=[
                {
                   "source_name": "DISARM",
                   "url": f"https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/generated_pages/tactics/{t[0]}.md",
                   "external_id": f"{t[0]}"
                }
            ],
            object_marking_refs=marking_id,
            created_by_ref=identity_id
        )
        utils.fs.add(tactic)
        tactics.append(tactic)

    return tactics