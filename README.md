# TF2BD Player List Converter

You will need Python 3.7+ to use this script

## Usage

`python3 convert_tf2bd.py <the player list to convert> [--out_file <the file to output>]`

Run `python3 convert_tf2bd.py --help` for more info

# Player List Generator

**Note: This project is not affiliated with MAC, nor does it represent the MAC project in any capacity**

## Manual Usage

Run `pull_both.py`, (or any of the `pull_[mcd/tacobot].py` files) manually with python to output a file

## API

Run the API by initiating the Flask app in `api.py` or building and running the Docker container, then `GET 127.0.0.1/list`.