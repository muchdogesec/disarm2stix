import os
import json
import requests
from stix2 import FileSystemStore
from datetime import datetime

file_system = "stix2_objects"
if not os.path.exists(file_system):
    os.makedirs(file_system)
fs = FileSystemStore("stix2_objects")

def get_version():
    with open('DISARM_VERSION', 'r') as file:
        first_line = file.readline()
    return first_line
def publish_datetime_format(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d").strftime("%Y%m%d%H%M%S%f")[:-3]

def load_file_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error loading JSON from {url}: {e}")
        return None