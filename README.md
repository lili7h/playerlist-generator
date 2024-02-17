# TF2BD Player List Converter

You will need Python 3.7+ to use this script

## Usage

`python3 convert_tf2bd.py <the player list to convert> [--out_file <the file to output>]`

Run `python3 convert_tf2bd.py --help` for more info

# Player List Generator

**Note: This project is not affiliated with MAC, nor does it represent the MAC project in any capacity**

## Manual Usage

Run `pull_both.py`, (or any of the `pull_[mcd/tacobot].py` files) manually with python to output a file

### The following scripts use in-terminal prompting to take input, and have no command-line parameters.

Run `convert_tf2bd.py` to convert a tf2bd playerlist into a MAC compatible one.

Run `update_list.py` to update an existing playerlist with the output from MCD and Tacobot. It will prompt you to change any existing verdicts.

Run `stats.py` to get the stats for a given playerlist file.



## API

Run the API by initiating the Flask app in `api.py` or building and running the Docker container, then `GET 127.0.0.1/list`.