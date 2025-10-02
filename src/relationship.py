import uuid
from src.helpers import utils
from stix2 import Relationship
from datetime import datetime

from src.common import NAMESPACE


def make_disarm_subtechnique_relationship(
    source, target, marking_id, identity_id, date, description, external_references
):

    relationship = Relationship(
        id="relationship--{}".format(
            uuid.uuid5(namespace=NAMESPACE, name="{}+{}".format(source, target))
        ),
        source_ref=source,
        target_ref=target,
        relationship_type="subtechnique-of",
        object_marking_refs=marking_id,
        created_by_ref=identity_id,
        created="2020-01-01T00:00:00.000Z",
        modified=datetime.strptime(date, "%Y-%m-%d"),
        description=description,
        external_references=external_references,
    )

    return relationship


def make_disarm_subtechnique_relationships(techniques, identity_id, marking_id, date):

    technique_ids = {}
    for technique in techniques:
        technique_ids[technique["external_references"][0]["external_id"]] = (
            technique["id"],
            technique["external_references"][0],
        )

    relationships = []
    for technique in techniques:
        if technique["x_mitre_is_subtechnique"]:
            source_ext_ref = technique["external_references"][0]
            technique_id, target_ext_ref = technique_ids[
                source_ext_ref["external_id"].split(".")[0]
            ]
            relationship = make_disarm_subtechnique_relationship(
                technique["id"],
                technique_id,
                marking_id,
                identity_id,
                date,
                description=f"{source_ext_ref['external_id']} is a sub-technique of {target_ext_ref['external_id']}",
                external_references=[source_ext_ref, target_ext_ref],
            )
            relationships.append(relationship)
            utils.fs.add(relationship)

    return relationships
