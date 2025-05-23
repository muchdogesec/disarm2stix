@echo off

REM Clone the repo if not already present
IF NOT EXIST "disarm2stix" (
    git clone https://github.com/infoepi/disarm2stix
)

cd disarm2stix

REM Create virtual environment if not already present
IF NOT EXIST "disarm2stix_venv" (
    python -m venv disarm2stix_venv
)

REM Activate the virtual environment
call disarm2stix_venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
pip install stix2 stix2-validator

REM Print a UUID to verify setup
python -c "import uuid; print(uuid.uuid4())"
