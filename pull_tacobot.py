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


def convert_data(players: dict) -> dict:
    logger.info(f"Transforming {len(players)} player objects into MAC Client format...")
    _player_records = {'records': {}}
    for player in players:
        _player_records['records'][convert_sid3_to_sid64(player['steamid'])] = {
            'custom_data': {'playerNote': 'Auto-extracted from pull_tacobot.py'},
            'verdict': 'Cheater',
            'previous_names': []
        }
    logger.success("Done.")
    return _player_records


def get_mac_format() -> dict:
    return convert_data(get_data(TACO_BOT_URL)['players'])
