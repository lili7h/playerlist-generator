import pull_mcd
import pull_tacobot
import sys
import json

from loguru import logger

if __name__ == "__main__":
    logger.info(f"Generating player list from MCD and TacoBot...")
    _mcd_players = pull_mcd.get_mac_format()
    _tb_players = pull_tacobot.get_mac_format()

    _combined = {'records': _mcd_players['records'] | _tb_players['records']}
    if len(sys.argv) == 1:
        with open('../data/playerlist.json', 'w') as h:
            h.write(json.dumps(_combined))
            logger.success(f"Wrote data out to 'playerlist.json'.")
    else:
        with open(sys.argv[1], 'w') as h:
            h.write(json.dumps(_combined))
            logger.success(f"Wrote data out to '{sys.argv[1]}'.")
