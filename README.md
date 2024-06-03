# disarm2stix

A command line tool that turns the DISARM framework into STIX 2.1 Objects.

## Before you get started

If you do not want to backfill, maintain, or support your own DISARM STIX objects check out CTI Butler which provides a fully manage database of these objects and more!

https://www.ctibutler.com/

## Overview

The [DISARM Framework](https://www.disarm.foundation/framework) in parts aims to provide a single knowledge-base for disinformation classifications.

In the way MITRE ATT&CK has provided a standard for contextual information about adversary tactics and techniques based on real-world observations, DISARM aims to do the same for disinformation.

This code is heavily based on the DISARM Foundations [DISARM-STIX2 repository](https://github.com/DISARMFoundation/DISARM-STIX2/). I decided to create a seperate codebase as that repository does not seem to be actively maintained.

The code in this repository;

1. Takes the latest DISARM data (`.xls` file)
2. Converts them to STIX 2.1 Objects
3. Stores the STIX 2.1 Objects in the file store

## Install

```shell
# get code
git clone https://github.com/muchdogesec/disarm2stix
cd disarm2stix
# create venv
python3 -m venv disarm2stix_venv
source disarm2stix_venv/bin/activate
# install requirements
pip3 install -r requirements.txt
```

### Versioning

Make sure to set the `DISARM_VERSION` correctly (see section "Shortcomings of this code" in this readme).

Line 1 of this file defines the DISARM version number.

Line 2 of this file defines the datetime (`YYYY-MM-DD`) the specified version on line 1 was published (will be used as `modified` time of objects.

## Run

Generate the STIX objects in the `stix2_objects/` folder;

```shell 
python3 disarm2stix.py
```

On each run, all objects will be completely regenerated.

## How it works

The DISARM foundation maintain an Excel copy of the DISARM Framework here:

```shell
https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx
```

This is downloaded on each request, and is used to generate the STIX 2.1 objects. Currently only the `techniques` and `tactics` tabs are used by this script.

## Mapping information

disarm2stix converts the corresponding DISARM object into the following STIX 2.1 object shown in the following table.

| DISARM    | STIX2                 |
|-----------|-----------------------|
| Matrix    | `x-mitre-matrix`      |
| Tactic    | `x-mitre-tactic`      |
| Technique | `attack-pattern`      |

This conversion (especially the STIX custom objects `x-`) is heavily inspired by MITRE ATT&CK STIX 2.1 Objects (see note on ATT&CK navigator).

Note, this code only considers the DISARM Red Framework at present.

### Marking Definition / Identity

These are hardcoded and imported from our [stix4doge repository](https://github.com/muchdogesec/stix4doge). Specifically these objects;

* Marking Definition: https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/marking-definition/disarm2stix.json
* Identity: https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/identity/disarm2stix.json

### Matrix

```json
{
    "type": "x-mitre-matrix",
    "spec_version": "2.1",
    "id": "x-mitre-matrix--<UUID V5>",
    "created_by_ref": "<IMPORTED IDENTITY OBJECT>",
    "created": "<DATE IN DISARM_VERSION FILE>",
    "modified": "<DATE IN DISARM_VERSION FILE>",
    "name": "DISARM Red Framework",
    "description": "Incident creator TTPs.",
    "tactic_refs": [
        "<LIST OF ALL x-mitre-tactic IN BUNDLE>",
	],
    "external_references": [
        {
            "source_name": "DISARM",
            "url": "https://www.disarm.foundation/",
            "external_id": "DISARM"
        }
    ],
    "object_marking_refs": [
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "<IMPORTED MARKING DEFINITION OBJECT>"
    ]
}
```

To generate the id, a UUIDv5 is generated using the namespace `8700e156-6ce9-5090-8589-f9d0aef7bdb7` and `DISARM Red Framework` which will always create the UUID `03e1a731-175d-5181-ba28-8be2e2159da9` = `x-mitre-matrix--03e1a731-175d-5181-ba28-8be2e2159da9`

### Tactic

```json
{
    "type": "x-mitre-tactic",
    "spec_version": "2.1",
    "id": "x-mitre-tactic--<UUID V5>",
    "created_by_ref": "<IMPORTED IDENTITY OBJECT>",
    "created": "<DATE IN DISARM_VERSION FILE>",
    "modified": "<DATE IN DISARM_VERSION FILE>",
    "name": "<name>",
    "description": "<summary>",
    "external_references": [
        {
           "source_name": "DISARM",
           "url": "https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/generated_pages/tactics/<tactic.disarm_id>.md",
           "external_id": "<tactic.disarm_id>"
        }
    ],
    "object_marking_refs": [
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "<IMPORTED MARKING DEFINTION OBJECTS>"
    ],
    "x_mitre_shortname": "<machine friendly name>"
}
```

To generate the id, a UUIDv5 is generated using the namespace `8700e156-6ce9-5090-8589-f9d0aef7bdb7` and `<tactic.disarm_id>`.

e.g. `TA05` = `10ccaa61-bf44-56ec-b1a7-3fc01942ec6d` = `x-mitre-tactic--10ccaa61-bf44-56ec-b1a7-3fc01942ec6d`

### Technique

```json
{
    "type": "attack-pattern",
    "spec_version": "2.1",
    "id": "attack-pattern--<UUID V5>",
    "created_by_ref": "<IMPORTED IDENTITY OBJECT>",
    "created": "<DATE IN DISARM_VERSION FILE>",
    "modified": "<DATE IN DISARM_VERSION FILE>",
    "name": "<name>",
    "description": "<summary>",
    "external_references": [
       {
            "source_name": "DISARM",
            "url": "https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/main/generated_pages/techniques/<technique.disarm_id>.md",
            "external_id": "<technique.disarm_id>"
        }
    ],
    "kill_chain_phases": [
       {
           "kill_chain_name": "DISARM",
           "phase_name": "<parent tactic machine friendly name>"
        }
    ],
    "x_mitre_is_subtechnique": "<boolean, if subtechique>",
    "x_mitre_platforms": [
        "Windows",
        "Linux",
        "Mac"
    ],
    "x_mitre_version": "2.1",
    "object_marking_refs": [
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "<IMPORTED MARKING DEFINTION OBJECTS>"
    ]
}
```

An object is determined to be a subtechnique if the `<technique.disarm_id>` contains a `.`. e.g. is a subtechnique `T0019.002`, is not a subtechnique `T0019`.

To generate the id, a UUIDv5 is generated using the namespace `8700e156-6ce9-5090-8589-f9d0aef7bdb7` and `<technique.disarm_id>`.

e.g. `T0086.003` = `00dc0ed2-b16d-5f33-bad3-cc54fb7be6a9` = `attack-pattern--00dc0ed2-b16d-5f33-bad3-cc54fb7be6a9`

### Relationships

DISARM contains a hierachical structure of data where a technique can have a child (a subtechnique). e.g parent = T0019 and child = T0019.002.

You can identify a subtechnique if the techniques `attack-pattern` object has a `x_mitre_is_subtechnique` equal to `true`. If this is the case, the following relationship is created;

```json
{
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--<UUIDV5 GENERATION LOGIC>",
    "created_by_ref": "<IMPORTED IDENTITY OBJECT>",
    "created": "<CREATED TIME OF MOST RECENT DISARM OBJECT IN PAIR>",
    "modified": "<CREATED TIME OF MOST RECENT DISARM OBJECT IN PAIR>",
    "relationship_type": "subtechnique-of",
    "source_ref": "attack-pattern--<CHILD OBJECT>",
    "target_ref": "attack-pattern--<PARENT OBJECT>",
    "object_marking_refs": [
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "<IMPORTED MARKING DEFINTION OBJECTS>"
    ],
}
```

To generate the id of the SRO, a UUIDv5 is generated using the namespace `8700e156-6ce9-5090-8589-f9d0aef7bdb7` and `<source_ref>+<target_ref>`.

e.g. `attack-pattern--bc07b77c-7af3-5471-9a11-09e458fbad1e+attack-pattern--8df661b8-5f4f-5e3e-bad8-371e0099e447` = `016a0f81-731e-5b3b-8fc3-8d0111fbf1c1` = `relationship--016a0f81-731e-5b3b-8fc3-8d0111fbf1c1`

### Bundle

disarm2stix also creates a STIX 2.1 Bundle JSON object containing all the other STIX 2.1 Objects created at each run. The Bundle takes the format;

```json
{
    "type": "bundle",
    "id": "bundle--<UUIDV5 GENERATION LOGIC>",
    "objects": [
        "<ALL STIX JSON OBJECTS>"
    ]
}
```

To generate the id, a UUIDv5 is generated using the namespace `8700e156-6ce9-5090-8589-f9d0aef7bdb7` and the MD5 file hash of all sorted objects in the bundle.

Unlike the other STIX Objects, this means on every update a new bundle ID will be generated (as the date changes in the UUIDv5 generation). This means each saved bundle provides a historic snapshot of the old versions, should a user ever need to retrieve them.

### MITRE ATT&CK Navigator integration

The output of this script is designed to work with MITRE ATT&CK Navigator.

https://github.com/mitre-attack/attack-navigator

You can upload the bundle to MITRE ATT&CK Navigator as follows;

1. Go to https://mitre-attack.github.io/attack-navigator/ (or your own Navigator install)
2. Select "create new layer"
3. Select "more options"
4. Enter the URL of your bundle in "Collection or STIX bundle URL"
5. Enter "Bundle version number" (can be any number)
6. Enter "Bundle domain"

## Shortcomings of this code

DISARM is versioned, but it is not easy to determine versions in a programmatic way.

[It appears versioning is done mostly in blog posts](https://medium.com/disarming-disinformation/disarm-update-version-1-3-9dfcf2a29864).

As such the `DISARM_VERSION` needs to be manually updated with both the version and `modified` time. The `created` time is hard coded as `2020-01-01T00:00:00.000Z` for all objects.

It is possible to grab specific version URL of the .xlsx file (using historic commits) and run this script using them. To do this, go into `helpers/file.py` and modify the variable `xlsx_url`.

https://github.com/DISARMFoundation/DISARMframeworks/commits/main/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx

For reference, here are the available versions and corresponding .xlsx files to use;

* 1.2 (2023-08-10): https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/382df9325af25e650667f81a3ff0575b2307b949/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx 
* 1.3 (2023-09-13): https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/62680c33d5cd1fabbc5aec4fa6390a0180ed3ea2/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx
* 1.4 (2024-03-13): https://raw.githubusercontent.com/DISARMFoundation/DISARMframeworks/f1ac3b04ee17388d9ccc1ada5ad4ed1160f01fe0/DISARM_MASTER_DATA/DISARM_FRAMEWORKS_MASTER.xlsx

## Useful supporting tools

* Existing STIX 2.1 schemas: [cti-stix2-json-schemas](https://github.com/oasis-open/cti-stix2-json-schemas): OASIS TC Open Repository: Non-normative schemas and examples for STIX 2
* To generate STIX 2.1 extensions: [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/)
* STIX 2.1 specifications for objects: [STIX 2.1 docs](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
* [DISARM Framework](https://www.disarm.foundation/framework)

## Support

[Minimal support provided via the DOGESEC community](https://community.dogesec.com/).

## License

[Apache 2.0](/LICENSE).