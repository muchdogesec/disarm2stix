from stix2 import AttackPattern, properties, ExternalReference
import objects.marking_definition
import pandas as pd
from objects import identity, marking_definition
from uuid import UUID
import uuid
from helpers import utils
from datetime import datetime

def make_disarm_techniques(data, identity_id, marking_id, date:str, remove_external=False):

    tacdict = pd.Series(data["tactics"].name.values, index=data["tactics"].disarm_id).to_dict()
    techniques = []
    for t in data["techniques"].values.tolist():
        external_references = [
            {
                'external_id': f'{t[0]}'.strip(),
                'source_name': 'DISARM',
                'url': f'https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/generated_pages/techniques/{t[0]}.md'
            }
        ]

        kill_chain_phases = [
            {
                'phase_name': tacdict[t[3]].replace(' ', '-').lower(),
                'kill_chain_name': 'disarm'
            }
        ]

        subtechnique = t[0].split(".")
        x_mitre_is_subtechnique = False
        if len(subtechnique) > 1:
            x_mitre_is_subtechnique = True

        x_mitre_platforms = 'Windows', 'Linux', 'Mac'
        if remove_external:
            external_references = []
            kill_chain_phases = []

        technique = AttackPattern(
            id="attack-pattern--{}".format(
                uuid.uuid5(namespace=UUID("8700e156-6ce9-5090-8589-f9d0aef7bdb7"), name=f"{t[0]}")),
            name=f"{t[1]}",
            description=f"{t[4]}",
            external_references=external_references,
            object_marking_refs=marking_id,
            created_by_ref=identity_id,
            kill_chain_phases=kill_chain_phases,
            custom_properties={
                'x_mitre_platforms': x_mitre_platforms,
                'x_mitre_version': "2.1",
                'x_mitre_is_subtechnique': x_mitre_is_subtechnique
            },
            created="2020-01-01T00:00:00.000Z",
            modified=datetime.strptime(date, '%Y-%m-%d'),

        )
        if not remove_external:
            utils.fs.add(technique)
            techniques.append(technique)
    return techniques