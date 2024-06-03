import helpers
from objects import tactic, technique, matrix, relationship, identity, marking_definition, bundle
from helpers import xlsx, file
import os
import shutil


def clean_filesystem():
    file_system = "stix2_objects"
    for filename in os.listdir(file_system):
        file_path = os.path.join(file_system, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
           print(f"Failed to delete {file_path}. Reason: {e}")

def generate_disarm_stix():
    helpers.file.download_file_from_url()
    data = helpers.xlsx.load_excel_data()
    clean_filesystem()
    file_data = file.read_file("DISARM_VERSION")


    disarm_identity = identity.make_disarm_identity()
    identity_id = disarm_identity[0]["id"]
    disarm_marking_definition = marking_definition.make_disarm_marking_definition(identity_id)
    marking_id = marking_definition.custom_md()
    tactics = tactic.make_disarm_tactics(data, identity_id, marking_id, file_data[1])
    techniques = technique.make_disarm_techniques(data, identity_id, marking_id,file_data[1])
    subtechnique_relationships = relationship.make_disarm_subtechnique_relationships(techniques,identity_id, marking_id,date=file_data[1])
    navigator_matrix = matrix.make_disarm_matrix(tactics, identity_id, marking_id, date=file_data[1])
    technique.make_disarm_techniques(data, identity_id, marking_id, remove_external=True,date=file_data[1])
    stix_objects = []
    stix_objects.append(tactics)
    stix_objects.append(techniques)
    stix_objects.append(subtechnique_relationships)
    stix_objects.append(disarm_identity)
    stix_objects.append(disarm_marking_definition)
    stix_objects.append(navigator_matrix)
    stix_objects = tactics + techniques + subtechnique_relationships + disarm_identity+ disarm_marking_definition+navigator_matrix
    helpers.file.write_bundle(stix_objects)
    bundle.make_stix_bundle(stix_objects)
    helpers.file.delete_file_from_folder()


if __name__ == "__main__":
    generate_disarm_stix()
