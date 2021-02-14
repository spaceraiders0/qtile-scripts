#!/usr/bin/env python

"""A script to handle switching wallpapers.
"""

import os
import sys
import definitions
from pathlib import Path
from configparser import ConfigParser

ROOT_DIR = Path(__file__).parent
WALLPAPER_STORAGE = Path("~/wallpapers/pictures").expanduser()
WALLPAPER_SETTINGS = ROOT_DIR / Path("settings.ini")
settings = ConfigParser()


class WallpaperManager():
    """Controls the wallpaper of the current user. Exposes several
    methods for retrieving and setting wallpaper.

    :param wallpapers: where the wallpapers are stored
    :type wallpapers: pathlib.Path, defaults to "" 
    :param use_settings: whether or not to generate a settings file to
            used by window manager configuration files.
    :type use_settings: bool, defaults to True
    :param recursive: whether or not to recursively retrieve wallpapers from a
            directory recursively or not.
    :type recursive: bool, defaults to True.
    """

    def __init__(self, wallpapers, use_settings: bool = True, recursive=True):
        self.uses_settings = use_settings

        # Make sure that the settings file exists if attempting to
        # store this information.
        if use_settings is True:
            if WALLPAPER_SETTINGS.exists() is False:
                definitions.generate_tree()

        self.wallpaper_source = Path(wallpapers).expanduser()
        self.wallpaper_index = 0
        self.wallpaper_path = self.wallpaper_cache[self.wallpaper_index]
 
        if recursive is True:
            self.wallpaper_cache = list(self.wallpaper_source.rglob("*"))
        else:
            self.wallpaper_cache = list(self.wallpaper_source.iterdir())


        # Load a backup wallpaper directory if none is found.
        if use_settings is True:
            # Generate the settings file.
            definitions.generate_tree()
            settings.read(WALLPAPER_SETTINGS)

            # Loads current settings into the class.
            try:
                self.wallpaper_index = int(settings["wallpaper"]["index"])
                self.wallpaper_path = self.wallpaper_cache[self.wallpaper_index]
            except IndexError:
                print("Malformed settings file. Index is out of bounds.")

    def _write(self):
        """Writes the current settings to the configuration file. This assumes
        that uses_settings is True.
        """

        settings["wallpaper"]["index"] = str(self.wallpaper_index)

        with open(WALLPAPER_SETTINGS, "w") as settings_file:
            settings.write(settings_file)

    def reload(self):
        """Reloads the wallpaper storage
        """

        self.wallpaper_cache = list(self.wallpaper_source.iterdir())

    def load(self):
        """Simply sets the wallpaper using the current settings.
        """

        try:
            wallpaper_to_load = self.wallpaper_cache[self.wallpaper_index]
            self.wallpaper_path = wallpaper_to_load
            os.system(f"feh --bg-fill {self.wallpaper_path}")
        except IndexError:
            print(f"Malformed settings. Index {self.wallpaper_index} could not be found!") 

    def load_index(self, index_to_load: int):
        """Loads a wallpaper from it's index in the cache.
        """

        # Make sure it is a valid position.
        if index_to_load >= 0 and index_to_load < len(self.wallpaper_cache):
            self.wallpaper_index = index_to_load

            if self.uses_settings is True:
                settings["wallpaper"]["index"] = str(index_to_load)
                self._write()

            self.load()
        else:
            raise IndexError(f"{index_to_load} is out wallpaper bounds!")

    def load_name(self, name: str):
        """Loads a wallpaper by finding it's index in the wallpaper_cache.

        :param name: the name to find
        :type name: str
        """

        for index, path in enumerate(self.wallpaper_cache):
            if path.name == name:
                self.load_index(index)

    def load_step(self, step: int = 1):
        """Retrieves the nth next wallpaper.

        :param step: how far to step.
        :type step: int
        """

        next_index = abs((self.wallpaper_index + step) % len(self.wallpaper_cache))
        self.load_index(next_index)

    def load_inc(self):
        """Loads the next wallpaper.
        """

        self.load_step(1)

    def load_dec(self):
        """Loads the previous wallpaper.
        """

        self.load_step(-1)

    def get_state(self) -> [str, str]:
        """Displays the state of the current wallpaper.
        """

        states = (
            f"Index: {self.wallpaper_index}",
            f"Path: {self.wallpaper_path}",
            f"Source: {self.wallpaper_source}",
        )

        return states

    def get_path(self) -> str:
        """Retrieves the path of the current wallpaper.
        """

        return self.wallpaper_path

    def get_index(self) -> int:
        """Retrieves the index of the current wallpaper.
        """

        return self.wallpaper_index


# Parse commands if this is being invoked.
if __name__ == "__main__":
    Manager = WallpaperManager(WALLPAPER_STORAGE)
    args = definitions.parse_args(sys.argv[1:])

    commands = {
        "get-state": Manager.get_state,
        "get-index": Manager.get_index,
        "get-path": Manager.get_path,
        "load-inc": Manager.load_inc,
        "load-dec": Manager.load_dec,
        "load-name": Manager.load_name,
        "load-step": Manager.load_step,
        "load-index": Manager.load_index,
        "load": Manager.load,
        "reload": Manager.reload,
    }

    # Execute a specific function here.
    try:
        if len(args) > 0:
            command = args.pop(0)

            if command in commands:
                result = commands[command](*args)

                if result is not None:
                    print(result)
            else:
                print(f"'{command}' is an invalid command.")
    except TypeError:
        print("Invalid number of arguments!")
