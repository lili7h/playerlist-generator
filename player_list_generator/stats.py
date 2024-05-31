import questionary
import os
import orjson
import requests
import datetime

from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError


EXPECTED_SCHEMA_URI_PROT = "https"
EXPECTED_SCHEMA_DOM = "lilithwolf.vip/"
EXPECTED_SCHEMA_PATH = "schemas/"

infile = questionary.path("Enter path to existing MAC playerlist file -> ").ask()
if infile is None:
    print(f"Cancelled by user, Exiting")
    exit(1)

if not os.path.exists(infile):
    print(f"Invalid path!")
    exit(1)

with open(infile, 'r', encoding='utf8') as h:
    _list = orjson.loads(h.read())

if "$schema" not in _list:
    print(f"WARN: That player list file doesn't have a $schema defined!")
else:
    print(f"Validating PlayerList by referenced schema...")
    _expected_schema_format = f"{EXPECTED_SCHEMA_URI_PROT}://{EXPECTED_SCHEMA_DOM}{EXPECTED_SCHEMA_PATH}"
    if not _list['$schema'].startswith(_expected_schema_format):
        print(f"ERR: Unexpected schema host/path combination, possible security violation, aborting.")
        print(f"ERR: {_list['$schema']} does not fit the expected format of '{_expected_schema_format}...'")
        exit(1)

    _schema_name = _list['$schema'].split('/')[-1]
    _schema_version = _schema_name.split('.')[-2]

    print(f"Identified schema version {_schema_version} ({_schema_name}) found at {_list['$schema']}")
    try:
        Draft202012Validator(
            requests.get(_list['$schema']).json(),
        ).validate(_list)
    except ValidationError as e:
        if not os.path.exists('../logs/'):
            os.mkdir('../logs')
        print(f"ERR: playerlist contained invalid json format according to its schema, potentially corrupt player file")
        _fn = Path(f"logs/pl-json-validation-err-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.txt")
        with open(_fn, 'w', encoding='utf8') as h:
            h.write(str(e))
        print(f"ERR: The validation error log has been written to file 'logs/{_fn.name}'.")
        exit(1)

    print("SUCCESS: playerlist json is valid!")


_num_player_objects = len(_list['records'].keys())
_num_cheaters = len([x for x in _list['records'] if _list['records'][x]['verdict'] == 'Cheater'])
_num_bots = len([x for x in _list['records'] if _list['records'][x]['verdict'] == 'Bot'])
_num_players = len([x for x in _list['records'] if _list['records'][x]['verdict'] == 'Player'])
_num_trusted = len([x for x in _list['records'] if _list['records'][x]['verdict'] == 'Trusted'])
_file_size = os.stat(infile).st_size / 1024

width = 48
print(f"+{'-'*(width-2)}+")
print(f"|{' '*((width-22)//2)}MAC playerlist Stats{' '*((width-22)//2)}|")
print(f"+{'-'*(width-2)}+")
print(f"| Total Tracked Players: {_num_player_objects}{' '*(width-26-len(str(_num_player_objects)))}|")
print(f"|      Tracked Cheaters: {_num_cheaters}{' '*(width-26-len(str(_num_cheaters)))}|")
print(f"|          Tracked Bots: {_num_bots}{' '*(width-26-len(str(_num_bots)))}|")
print(f"|       Tracked Players: {_num_players}{' '*(width-26-len(str(_num_players)))}|")
print(f"|       Trusted Players: {_num_trusted}{' '*(width-26-len(str(_num_trusted)))}|")
print(f"|       Total File size: {_file_size:.2f}kb{' '*(width-28-len(str(f'{_file_size:.2f}')))}|")
print(f"+{'-'*(width-2)}+")