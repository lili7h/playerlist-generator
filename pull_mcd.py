import requests
import json5
import json
import datetime

from bs4 import BeautifulSoup
from loguru import logger


MCD_URL: str = "https://megascatterbomb.com/mcd"
COLOUR_TO_VERDICT_MAP: dict = {
    "#ffffff": "Player",
    "#ff3300": "Cheater",
    "#33ff00": "Trusted",
    "#ffff00": "Suspicious",
    "#00ffff": "Trusted",
}


def pull_html(url: str, encoding: str = 'utf8') -> str:
    logger.info(f"Requesting {url}, decoding to {encoding}...")
    response = requests.get(url)
    logger.success(f"Done.")
    return response.content.decode(encoding)


def parse_html(html: str) -> list[dict]:
    logger.info(f"Parsing {len(html)} characters of HTML...")
    _soup = BeautifulSoup(html, "html5lib")
    _script_elems = _soup.find_all("script")
    _js: str = _script_elems[1].string
    _open_str = "var nodes = new vis.DataSet("
    _close_str = "var edges = new vis.DataSet"
    _players = _js[_js.index(_open_str) + len(_open_str):_js.index(_close_str)-4]
    logger.success(f"Done.")
    logger.info(f"Extracting {len(_players)} characters of JS variables into a native dictionary...")
    # json5 loads absolutely slaughters the interpreter performance on js objs of this size
    _dict = json5.loads(_players)
    logger.success(f"Done.")
    return _dict


def parse_to_mac_playerrecords_format(mcd_objects: list[dict]) -> dict:
    logger.info(f"Transforming {len(mcd_objects)} player objects into MAC Client format...")
    _player_records = {'records': {}}
    _current_time = datetime.datetime.now().isoformat() + 'Z'

    for player in mcd_objects:
        _player_records['records'][player['id']] = {
            'custom_data': {'playerNote': 'Auto-extracted from pull_mcd.py'},
            'verdict': COLOUR_TO_VERDICT_MAP[player['color']['background']],
            'previous_names': player['aliases'],
            'modified': _current_time,
            'created': _current_time,
        }
    logger.success("Done.")
    return _player_records


def get_mac_format() -> dict:
    return parse_to_mac_playerrecords_format(parse_html(pull_html(MCD_URL)))


# print(pull_html(MCD_URL))


if __name__ == "__main__":
    print(f"Extracting player list from MCD...")
    _playerlist_mcd = parse_to_mac_playerrecords_format(parse_html(pull_html(MCD_URL)))
    with open('playerlist.json', 'w') as h:
        h.write(json.dumps(_playerlist_mcd))
        print(f"Wrote data out to 'playerlist.json'.")
    print(f"Done.")
