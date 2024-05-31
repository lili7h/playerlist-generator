import questionary
import os.path
import pull_mcd
import pull_tacobot
import orjson
import datetime

from loguru import logger


infile = questionary.path("Enter path to existing MAC playerlist file -> ").ask()
if infile is None:
    print(f"Cancelled by user, Exiting")
    exit(1)

if not os.path.exists(infile):
    print(f"Invalid path!")
    exit(1)

_mcd_players = pull_mcd.get_mac_format()
_tb_players = pull_tacobot.get_mac_format()
_combined = {'records': _mcd_players['records'] | _tb_players['records']}

with open(infile, 'r', encoding='utf8') as h:
    _current = orjson.loads(h.read())

_new_records: int = 0
_existing_records: int = len(_current['records'].keys())
_updated_records: int = 0
for _possible_new in _combined['records']:
    if _possible_new in _current['records']:
        _past_names = _combined['records'][_possible_new]['previous_names']
        _possible_name = _past_names[0] if len(_past_names) > 0 else _possible_new

        _new_verdict = _combined['records'][_possible_new]['verdict']
        _old_verdict = _current['records'][_possible_new]['verdict']
        if _new_verdict != _old_verdict:
            if _new_verdict == 'Cheater' and _old_verdict == 'Bot':
                continue
            logger.warning(f"Verdict for player '{_possible_name}' changed from '{_old_verdict}' to '{_new_verdict}'.")
            update_verdict = questionary.confirm(f"Would you like to keep the original verdict? "
                                                 f"(No will replace the old verdict with the new one)").ask()
            if update_verdict:
                _current['records'][_possible_new]['verdict'] = _new_verdict
                _updated_records += 1
        continue
    else:
        _past_names = _combined['records'][_possible_new]['previous_names']
        _possible_name = _past_names[0] if len(_past_names) > 0 else _possible_new
        logger.info(f"Added new data for new record for '{_possible_name}'")
        _current_time = datetime.datetime.now().isoformat()

        _current['records'][_possible_new] = _combined['records'][_possible_new]
        _new_records += 1

logger.info(f"Completed merging, performing validity checks...")
with open(infile, 'r', encoding='utf8') as h:
    _old = orjson.loads(h.read())

for _old_player in _old['records']:
    if _old_player not in _current['records']:
        _current['records'][_old_player] = _old['records']['_old_player']
        logger.info(f"Re-added information regarding '{_old_player}' as it was somehow lost")

outfile = questionary.path("Enter path to save new MAC playerlist file -> ").ask()
if outfile is None:
    print(f"No path provided, dumping to stdout")
    print(orjson.dumps(_current))
    exit(1)

with open(outfile, 'wb') as h:
    h.write(orjson.dumps(_current))
    print(f"Saved new list to {outfile}.")
    exit(0)
