# qtile-scripts
Scripts I have created for the dynamic tiling window manager, QTile.

## Wallpaper Switcher
A script to control the current wallpaper. It comes with a ton of commands to load different wallpapers, and retrieve information about them. These can be invoked using the module itself in a script, or by executing the script through the shell.
```
get-state: Returns information about the state of the program. Specifically:
           - The wallpaper's index
           - The wallpaper's path
           - The directory the wallpaper is stored in.

get-index: Returns the index of the current wallpaper.
get-path: Returns the path of the current wallpaper.
load-inc: Loads the next wallpaper.
load-dec: Loads the previous wallpaper.
load-name: Load the wallpaper according to it's name.
load-step: Loads the next or previous wallpaper n steps back or ahead.
load-index: Loads a wallpaper from a specific index.
load: Simply loads the wallpaper according to the settings.
reload: Reloads the wallpaper cache.
```

Here is an example of how to load wallpapers from the Photos directory (if you have it):

```python
from wallpaper_switcher import WallpaperManager as WM

myWM = WM("~/Photos", use_settings=False)
myWM.load_name("my_dog.jpg")
```

This will load a file called "my_dog.jpg" from the folder. There is also an option to recursively retrieve files from your directory of choice recursively, which is described in the documentation. This also allows for loading your previous wallpapers on startup. For example, in my configuration, I have the following:

```python
@hook.subscribe.startup
def on_restart():
    subprocess.Popen([f"{PATHS['wallpaper_switcher']}", "load"])
    subprocess.Popen(["wal", "-R"])
    qtile_defs.on_restart()
```

Which invokes the script, and loads the previously saved wallpaper. However, while using this method to save wallpapers across reboots is *definitely* the way to go if you choose to use this, this does require you use the settings parameter to save which wallpaper is currently in use. The settings file is created in the same directory as the script, so it should be easy to find.
