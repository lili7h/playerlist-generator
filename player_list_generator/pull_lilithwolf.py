import requests
import json
from datetime import datetime

from loguru import logger

WOLF_URL: str = "https://lilithwolf.vip/lists/"
LIST_NAMES: list[str] = ["cheater.txt", "suspicious.txt", "watch.txt"]


def pull_html(url: str, encoding: str = 'utf8') -> str:
    logger.info(f"Requesting {url}, decoding to {encoding}...")
    response = requests.get(url)
    logger.success(f"Done.")
    return response.content.decode(encoding)


def aggregate_lists(wolf_url: str, list_names: list[str]) -> list[dict]:
    verdict_mapping: dict[str, str] = {
        "cheater.txt": "Cheater",
        "suspicious.txt": "Suspicious",
        "watch.txt": "Player",
    }

    output = []
    lists = [pull_html(wolf_url + ln, 'ANSI') for ln in list_names]
    for idx, wolf_list in enumerate(lists):
        _entries = wolf_list.split("\n")
        for entry in _entries:
            if entry is None or entry.strip() == "":
                continue
            _tuple = tuple([x.strip() for x in entry.split("-", maxsplit=1)])
            try:
                _sid64, _name = _tuple
            except ValueError as e:
                print(_tuple)
                raise e
            player_dict = {
                'id': _sid64,
                'name': _name,
                'verdict': verdict_mapping[LIST_NAMES[idx]],
            }
            _note = None
            match player_dict['verdict']:
                case 'Player':
                    _note = "Was marked as suspicious by M"
                case 'Cheater':
                    _note = "Was marked as blatant by M"
                case 'Suspicious':
                    _note = "Was marked as closet by M"
            player_dict['note'] = _note
            output.append(player_dict)

    return output


def parse_to_mac_playerrecords_format(wolf_objects: list[dict]) -> dict:
    logger.info(f"Transforming {len(wolf_objects)} player objects into MAC Client format...")
    _player_records = {'records': {}}
    _current_time = datetime.now().isoformat() + 'Z'

    for player in wolf_objects:
        _player_records['records'][player['id']] = {
            'custom_data': {'playerNote': f'[wolflist] {player["note"]}'},
            'verdict': player['verdict'],
            'previous_names': [player['name']],
            'modified': _current_time,
            'created': _current_time,
        }
    logger.success("Done.")
    return _player_records


def get_mac_format() -> dict:
    return parse_to_mac_playerrecords_format(aggregate_lists(WOLF_URL, LIST_NAMES))


if __name__ == "__main__":
    print(f"Extracting player list from Lilithwolf...")
    _playerlist_mcd = get_mac_format()
    with open('../output/wolf.json', 'w') as h:
        h.write(json.dumps(_playerlist_mcd))
        print(f"Wrote data out to 'wolf.json'.")
    print(f"Done.")
