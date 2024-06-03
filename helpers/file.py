import json
import os
from stix2 import Bundle
import shutil
import requests
import uuid
from uuid import UUID

def write_disarm_dir(dir):
    try:
        os.mkdir('stix2_objects/')
    except FileExistsError:
        pass

    try:
        os.mkdir('stix2_objects/' + dir)
    except FileExistsError:
        pass

def clean_stix2_objects_dir():
    """Recursively delete the stix2_objects folder.

    Returns:

    """
    shutil.rmtree("stix2_objects/")

def write_file(file_name, file_data):
    with open(file_name, 'w') as f:
        # f.write(json.dumps(file_data, sort_keys=True, indent=4))
        f.write(file_data.serialize(pretty=True))
        f.write('\n')


def write_files(folder, file_name, stix_objects):
    id = "bundle--" + str(uuid.uuid5(namespace=UUID('e9988722-c396-5a91-a08d-db742bd3624b'),name='DISARM Framework+1.3'))
    bundle = Bundle(id=id, objects=stix_objects, allow_custom=True)
    write_json_file(
        folder,
        file_name,
        json.loads(bundle.serialize()),
    )


def write_json_file(folder, filename, data):
    if not os.path.exists(folder):
        os.makedirs(folder)
    json_file = os.path.join(folder, filename)
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


def write_bundle(bundle):
    write_files(f"stix2_objects","disarm-bundle.json", bundle)

def download_file_from_url():
    file_name = "DISARM_FRAMEWORKS_MASTER.xlsx"
    # latest xlsz_url = https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx but check the version of the framework first if using this URL!
    xlsx_url = "https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/f1ac3b04ee17388d9ccc1ada5ad4ed1160f01fe0/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx"
    response = requests.get(xlsx_url)
    if response.status_code == 200:
        # Open the file for writing in binary mode
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded '{os.path.basename(xlsx_url)}' and saved it to '{file_name}'")
    else:
        print(f"Failed to download '{xlsx_url}'")

def delete_file_from_folder():
    file_to_delete = 'DISARM_FRAMEWORKS_MASTER.xlsx'
    if os.path.exists(file_to_delete):
        try:
            os.remove(file_to_delete)
            print(f"File '{file_to_delete}' has been successfully deleted.")
        except OSError as e:
            print(f"Error: {e}")
    else:
        print(f"File '{file_to_delete}' does not exist.")


def read_file(filename):
    with open(filename, 'r') as file:
        file_lines = file.readlines()

    return file_lines