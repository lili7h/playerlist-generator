import sys
import json


def main():
    # If not appropriate Command Line Arg provided, exit early
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/mac/list")
        exit(1)

    cheaters = []
    suspicious = []
    friends = []

    # Read input MAC playerlist
    with open(sys.argv[1], 'r', encoding='ANSI') as h:
        data = json.load(h)
        records = data['records']

    # Iterate MAC records. Record is the SteamID64
    for record in records:
        _value = records[record]
        # Most MAC records will have a set of previous names, but some won't
        if len(_value['previous_names']):
            _previous_name = _value['previous_names'][0]
        else:
            _previous_name = "NONAME"

        # Match the MAC verdict to the NC file
        _str = f"{record} - {_previous_name}"
        match _value['verdict']:
            case 'Cheater':
                cheaters.append(_str)
            case 'Suspicious':
                suspicious.append(_str)
            case 'Trusted':
                friends.append(_str)

    # Write out files
    with open('Cheater.txt', 'w', encoding='ANSI') as h:
        h.write("\n".join(cheaters))

    with open('Suspicious.txt', 'w', encoding='ANSI') as h:
        h.write("\n".join(suspicious))

    with open('Ignore.txt', 'w', encoding='ANSI') as h:
        h.write("\n".join(friends))


if __name__ == "__main__":
    main()
