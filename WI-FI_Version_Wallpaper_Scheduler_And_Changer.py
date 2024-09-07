# Original Code from rhawk117 forked and majorly edited by Josh-Alley20
#
# Made for the scheduled switching of wallpapers on Windows
#
# 9/5/2024
#
# edits by rhawk117 on 9/6/2024

import os
import shutil
import subprocess
import ctypes
from pathlib import Path
import logging
import requests  # Import the requests library for downloading images


def combine(base, file_name) -> str:
    return os.path.join(base, file_name)


class APP_PATHS:
    BASE = r'C:\auto_wallpaper_switcher'
    BAT_FILE = combine(BASE, 'wallpaper_scheduler.bat')
    PYTHON_FILE = combine(BASE, 'wallpaper_afternoon.py')
    DESKTOP = Path.home() / 'Desktop'
    LOG_FILE = combine(BASE, 'wallpaper_switcher.log')


class IMAGE_FILES:
    ESC_ROOM = "Escape_Room_WP.png"
    CTF = "CTF_WP.png"

    # Replace with the raw GitHub URL to your images
    ESC_ROOM_URL = "https://raw.githubusercontent.com/Josh-Alley20/usb_wallpaper_aid/main/Escape_Room_WP.png"
    CTF_URL = "https://raw.githubusercontent.com/Josh-Alley20/usb_wallpaper_aid/main/CTF_WP.png"

    @staticmethod
    def base(file_name: str) -> str:
        return combine(APP_PATHS.BASE, file_name)


def download_image(url: str, dest_path: str) -> None:
    """Download image from the provided URL to the destination path."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses
        with open(dest_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        logging.info(f'Downloaded image from {url} to {dest_path}')
    except Exception as e:
        logging.error(f'Failed to download image from {url}. Error: {e}')


def setup_logging_and_create_folder(path: str) -> None:
    """
        Create folder if it doesn't exist and set up logging.
    """
    try:
        os.makedirs(path, exist_ok=True)
        print(f'Created or verified folder: {path}')
    except Exception as e:
        print(f'Failed to create folder: {path}. Error: {e}')

    # Setup logging
    logging.basicConfig(
        filename=APP_PATHS.LOG_FILE,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(f'Logging initialized in {APP_PATHS.LOG_FILE}')


def write_file(file_path: str, content: str) -> None:
    """Write content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f'File written: {file_path}')
    except Exception as e:
        logging.error(f'Failed to write file: {file_path}. Error: {e}')


def create_python_script() -> None:
    """Create Python script to change wallpaper."""
    python_content = f"""import ctypes
import shutil
import os
from pathlib import Path

SPI_SETDESKWALLPAPER = 20
desktop = Path.home() / 'Desktop'
wallpaper_path = r'{IMAGE_FILES.base(IMAGE_FILES.ESC_ROOM)}'

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
"""
    write_file(APP_PATHS.PYTHON_FILE, python_content)


def create_bat_file() -> None:
    """Create batch file to run the Python script."""
    bat_content = f"""@echo off
cd {APP_PATHS.BASE}
python {APP_PATHS.PYTHON_FILE}
"""
    write_file(APP_PATHS.BAT_FILE, bat_content)


def schedule_task(task_name: str, bat_file_path: str, time, date) -> None:
    """Schedule a Windows task to run a batch file."""
    schedule_command = (
        f'schtasks /create /tn "{task_name}" /tr "{bat_file_path}" /sc once /st {time} /sd {date} /f'
    )
    logging.info(f'Executing command: {schedule_command}')
    try:
        subprocess.run(schedule_command, shell=True, check=True)
        logging.info(f'Task "{task_name}" created to run on {date} at {time}.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to create the scheduled task. Error: {e}')


def change_current_wallpaper() -> None:
    """Change the current wallpaper to CTF_WP.png."""
    SPI_SETDESKWALLPAPER = 20
    desktop = Path.home() / 'Desktop'
    wallpaper_path = IMAGE_FILES.base(IMAGE_FILES.CTF)

    try:
        # Copy wallpaper to the desktop
        shutil.copy(wallpaper_path, desktop)
        logging.info(f'Copied wallpaper to desktop: {wallpaper_path}')

        # Set the wallpaper
        wallpaper_on_desktop = combine(APP_PATHS.DESKTOP, IMAGE_FILES.CTF)
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            wallpaper_on_desktop,
            3
        )
        logging.info(f'Set wallpaper: {wallpaper_on_desktop}')

        # Delete the wallpaper from the desktop
        os.remove(wallpaper_on_desktop)
        logging.info(f'Removed wallpaper from desktop: {wallpaper_on_desktop}')
    except Exception as e:
        logging.error(f'Failed to change wallpaper. Error: {e}')


def main() -> None:
    setup_logging_and_create_folder(APP_PATHS.BASE)

    # Download images from GitHub
    download_image(IMAGE_FILES.ESC_ROOM_URL, IMAGE_FILES.base(IMAGE_FILES.ESC_ROOM))
    download_image(IMAGE_FILES.CTF_URL, IMAGE_FILES.base(IMAGE_FILES.CTF))

    create_python_script()
    create_bat_file()

    schedule_task(
        task_name='WallpaperSchedulerTask',
        bat_file_path=APP_PATHS.BAT_FILE,
        time='12:00',
        date='09/12/2024'
    )  # change this to set a different date and time.

    change_current_wallpaper()


if __name__ == '__main__':
    main()
