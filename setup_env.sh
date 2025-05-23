#!/bin/bash

# Clone the repo if not already present
if [ ! -d "disarm2stix" ]; then
  git clone https://github.com/muchdogesec/disarm2stix
fi

cd disarm2stix

# Create virtual environment if it doesn't exist
if [ ! -d "disarm2stix_venv" ]; then
  python3 -m venv disarm2stix_venv
fi

# Activate the virtual environment
source disarm2stix_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install stix2 stix2-validator

# Print a UUID to verify setup
python -c "import uuid; print(uuid.uuid4())"
