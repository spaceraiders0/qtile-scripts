#!/usr/bin/python3

"""Common methods, and other utilities used by the scripts.
"""

import re
import sys
from pathlib import Path

# Regular Expressions
INVALID_NAME = "^\s"
BOOL = "^((t|T)rue|(f|F)alse)"
FLOAT = "\d*\.\d+"
INT = "\d+"

SCRIPT_DIR = Path(__file__).parent
SETTINGS_FILE = SCRIPT_DIR / Path("settings.ini")
SETTINGS_TEMPLATE = """\
[wallpaper]
index = 0
wallpapers = ~/pictures/ 
"""


def parse_args(arg_list: str) -> list:
    """Parses a list of arguments and typecasts them.

    :param arg_list: the list containing all the arguments.
    :type arg_list: list
    :return: the casted arguments
    :rtype: list
    """

    parsed_args = []

    for arg in arg_list:
        if re.match(FLOAT, arg):
            parsed_args.append(float(arg))
        elif re.match(INT, arg):
            parsed_args.append(int(arg))
        elif re.match(BOOL, arg):
            parsed_args.append(bool(arg))
        else:
            parsed_args.append(arg)

    return parsed_args


def generate_tree():
    """Generates the settings.ini file used by each script.
    """

    if SETTINGS_FILE.exists() is False:
        with open(SETTINGS_FILE, "w") as new_file:
            new_file.write(SETTINGS_TEMPLATE)


if __name__ == "__main__":
    commands = {
            "rebuild": generate_tree
            }

    # Execute a specific function here.
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command in commands:
            commands[command]()
        else:
            print(f"'{command}' is an invalid command.")
