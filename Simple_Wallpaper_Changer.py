import ctypes
import shutil
import os
from pathlib import Path

SPI_SETDESKWALLPAPER = 20
desktop = Path.home() / 'Desktop'
wallpaper_path = r'C:\auto wallpaper switcher\Escape_Room_WP.png' # change to pic location

# Copy wallpaper to the desktop
shutil.copy(wallpaper_path, desktop)

# Set the wallpaper
wallpaper_on_desktop = str(desktop / Path(wallpaper_path).name)
ctypes.windll.user32.SystemParametersInfoW(
    SPI_SETDESKWALLPAPER,
    0,
    wallpaper_on_desktop,
    3
)

# Delete the wallpaper from the desktop
os.remove(wallpaper_on_desktop)
