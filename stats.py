import questionary
import os
import pull_mcd
import pull_tacobot
import orjson

from loguru import logger


infile = questionary.path("Enter path to existing MAC playerlist file -> ").ask()
if infile is None:
    print(f"Cancelled by user, Exiting")
    exit(1)

if not os.path.exists(infile):
    print(f"Invalid path!")
    exit(1)

with open(infile, 'r', encoding='utf8') as h:
    _list = orjson.loads(h.read())

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