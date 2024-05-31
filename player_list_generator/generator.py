import json
import sys
import os
import pathlib

from loguru import logger

import pull_mcd
import pull_tacobot
import pull_lilithwolf


NAME_MAP: dict[str, str] = {
    "wolf": "wolflist",
    "taco": "Tacobot",
    "mcd": "MCD",
}


def get_sets(existing_set: dict = None, priority=None) -> dict:
    """
    Aggregate all the lists from various sources into one location. There is a priority applied, where lists may not
    override the entries of a higher priority list. This lets you put the lists you 'trust' to be most accurate first,
    in case there are overlaps between the lists (there will very likely be).

    :param existing_set: An existing MAC format dictionary to merge at priority -1 (it comes first!)
    :param priority: A list of strings describing the order (first to last) in which player records should be entered.
                     Once a player record is entered, it will not be overwritten. Thus, this is also the order of
                     priority. Defaults to MCD -> Wolflist -> Tacobot (["mcd", "wolf", "taco"])
    :return: The newly minted MAC format dictionary
    """
    if priority is None:
        priority = ["mcd", "wolf", "taco"]

    _wolf = pull_lilithwolf.get_mac_format()
    _taco = pull_tacobot.get_mac_format()
    _mcd = pull_mcd.get_mac_format()

    prio_mapping: dict[str, dict] = {
        "wolf": _wolf,
        "taco": _taco,
        "mcd": _mcd,
    }

    _new_records = {} if existing_set is None else existing_set['records']
    _joined = {"records": _new_records}
    if _new_records != {}:
        logger.info(f"Initialised with {len(_new_records.keys())} player records from input file.")

    _clashes = 0
    for i in range(len(priority)):
        for entry in prio_mapping[priority[i]]['records']:
            if entry in _joined['records']:
                if 'custom_data' not in _joined['records'][entry]:
                    _joined['records'][entry]['custom_data'] = {}
                if 'playerNote' not in _joined['records'][entry]['custom_data']:
                    _joined['records'][entry]['custom_data']['playerNote'] = ""

                if _joined['records'][entry]['custom_data']['playerNote'] == "":
                    _joined['records'][entry]['custom_data']['playerNote'] += f"([{NAME_MAP[priority[i]]}])"
                else:
                    _joined['records'][entry]['custom_data']['playerNote'] += (f" (also in [{NAME_MAP[priority[i]]}] "
                                                                               f"list)")
                logger.debug(f"Clash on entry '{entry}', from list [{NAME_MAP[priority[i]]}] at priority {i}.")
                _clashes += 1
            else:
                _joined['records'][entry] = prio_mapping[priority[i]]['records'][entry]

    logger.info(f"The priority configuration of ({priority}) resolved {_clashes} entry clashes.")
    return _joined


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print(f"USAGE: {sys.argv[0]} outfile [input_file]")
        print(f"Where [input_file] is an optional file path to an existing file to merge into the"
              f" output with highest priority (i.e. other lists cannot replace their values)")
        exit(1)

    outfile: pathlib.Path = pathlib.Path(sys.argv[1])
    infile: pathlib.Path | None = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else None

    if outfile.exists():
        print("That file already exists, cowardly refusing to overwrite an existing file.")
        exit(1)

    _existing = None
    if infile is not None:
        if not infile.exists():
            print("The specified input file does not exist. Refusing to continue without it!")
            exit(1)

        with open(infile, 'r', encoding='ANSI') as h:
            try:
                data = json.load(h)
            except json.JSONDecodeError as e:
                logger.critical(f"Failed to interpret the input file as JSON. Is it really JSON?")
                raise e

        logger.info(f"Loaded existing player records file from {infile}.")
        _existing = data

    logger.info("Aggregating lists...")
    _new_file = get_sets(_existing)
    logger.success("Complete!")

    logger.info(f"Writing output to {outfile}...")
    with open(outfile, 'w') as h:
        try:
            json.dump(_new_file, h)
        except (TypeError, ValueError) as e:
            logger.critical(f"Failed to write the file due to bad data in the generated list. Contact the dev!")
            raise e
