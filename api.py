import os
import pull_mcd
import pull_tacobot
import json

from loguru import logger
from datetime import datetime
from flask import Flask


VERSION: str = "0.1.0a"

app = Flask(f"MAC PlayerList API v{VERSION}")


@app.route("/list", methods=["GET"])
def get_player_list():
    logger.info(f"GET /list called")

    cached_file_path = 'cache/playerlist.json'
    if os.path.exists(cached_file_path):
        logger.info(f"Cached playerlist.json detected...")
        stat = os.stat(cached_file_path)
        if (datetime.now() - datetime.fromtimestamp(stat.st_ctime)).days >= 1:
            logger.info(f"Cached playerlist.json is stale, removing...")
            os.remove(cached_file_path)
        else:
            logger.info(f"Cached playerlist.json is fresh, continuing...")
            with open(cached_file_path, 'r') as h:
                pl_json = h.read()
            logger.success(f"Returning {len(pl_json)} characters of json...")
            return pl_json

    logger.info(f"Generating fresh playerlist.json from mcd and tacobot...")
    _mcd_players = pull_mcd.get_mac_format()
    _tb_players = pull_tacobot.get_mac_format()

    _combined = {'records': _mcd_players['records'] | _tb_players['records']}
    _json_combined = json.dumps(_combined)
    with open(cached_file_path, 'w') as h:
        h.write(_json_combined)
    logger.info(f"Cached new playerlist.json at {cached_file_path}")

    logger.success(f"Returning {len(_json_combined)} characters of json...")
    return _json_combined


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

