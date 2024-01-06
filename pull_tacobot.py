import requests

from loguru import logger


TACO_BOT_URL: str = "https://api.tacobot.tf/public/tf2bd/v1"


def convert_sid3_to_sid64(sid3: str) -> str:
    steamid64ident = 76561197960265728
    return f"{steamid64ident + int(sid3.replace('[', '').replace(']','').split(':')[2])}"


def get_data(url: str) -> dict:
    logger.info(f"Requesting {url}, decoding from json...")
    response = requests.get(url)
    logger.success("Done.")
    return response.json()


def convert_data(players: dict, *, custom_note: str = None) -> dict:
    logger.info(f"Transforming {len(players)} player objects into MAC Client format...")
    _note = 'Auto-extracted from pull_tacobot.py' if custom_note is None else custom_note
    _player_records = {'records': {}}
    for player in players:
        _prevs: list[str]
        _custom_note = _note

        if 'last_seen' in player and 'player_name' in player['last_seen']:
            _prevs = player['last_seen']['player_name']
        else:
            _prevs = []

        if 'cheater' in player["attributes"]:
            _verdict = 'Cheater'
        else:
            _verdict = 'Player'
            _note = "Marked for: " + ", ".join(player["attributes"])

        _player_records['records'][convert_sid3_to_sid64(player['steamid'])] = {
            'custom_data': {'playerNote': _note},
            'verdict': _verdict,
            'previous_names': _prevs
        }
    logger.success("Done.")
    return _player_records


def get_mac_format() -> dict:
    return convert_data(get_data(TACO_BOT_URL)['players'])
