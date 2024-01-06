import argparse
import json

from pull_tacobot import convert_data

parser = argparse.ArgumentParser(
    prog="TF2BD to MAC Playerlist Converter",
    description="Converts TF2BD style json player lists into MAC compatible playerlists",
    epilog="This tool is provided as is, with absolutely no warranty. :)"
)

parser.add_argument('in_file', help='The input TF2BD playerlist file')
parser.add_argument(
    '--out_file',
    help='The file to output once everything is converted, default is "./playerlist.json"',
    default='./playerlist.json'
)

args = parser.parse_args()

with open(args.in_file, 'r') as h:
    data = json.load(h)

output = convert_data(data['players'], custom_note='Converted from TF2BD list by automation.')

with open(args.out_file, 'w') as h:
    h.write(json.dumps(output))
