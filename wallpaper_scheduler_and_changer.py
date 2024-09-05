#
# Original Code from rhawk117 forked and majorly edited by Josh-Alley20
#
# Made for the scheduled switching of wallpapers on windows
#
# 9/5/2024
#

import os
import shutil
import subprocess
import ctypes
from pathlib import Path
import logging

# Define paths
FOLDER_PATH = 'C:\\auto_wallpaper_switcher'
BAT_FILE_PATH = os.path.join(FOLDER_PATH, 'wallpaper_scheduler.bat')
PYTHON_FILE_PATH = os.path.join(FOLDER_PATH, 'wallpaper_afternoon.py')
DESKTOP_PATH = Path.home() / 'Desktop'
LOG_FILE_PATH = os.path.join(FOLDER_PATH, 'wallpaper_switcher.log')
WALLPAPER_SOURCE_IMAGES = ['D:\\CTF_WP.png', 'D:\\Escape_Room_WP.png']  # pulls desktop photos from usb drive change this to edit photos location or name.
WALLPAPER_PATH = os.path.join(FOLDER_PATH, 'Escape_Room_WP.png')
WALLPAPER_PATH_CURRENT = os.path.join(FOLDER_PATH, 'CTF_WP.png')

def setup_logging_and_create_folder(path):
    """Create folder if it doesn't exist and set up logging."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f'Created or verified folder: {path}')
    except Exception as e:
        print(f'Failed to create folder: {path}. Error: {e}')
        raise

    # Setup logging
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(f'Logging initialized in {LOG_FILE_PATH}')

def copy_images_to_folder(source_images, destination_folder):
    """Copy images from source to destination folder."""
    for image in source_images:
        if os.path.exists(image):
            try:
                shutil.copy(image, destination_folder)
                logging.info(f'Copied {image} to {destination_folder}')
            except Exception as e:
                logging.error(f'Failed to copy {image} to {destination_folder}. Error: {e}')
        else:
            logging.warning(f'File not found: {image}')

def write_file(file_path, content):
    """Write content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f'File written: {file_path}')
    except Exception as e:
        logging.error(f'Failed to write file: {file_path}. Error: {e}')

def create_python_script():
    """Create Python script to change wallpaper."""
    python_content = f"""import ctypes
import shutil
import os
from pathlib import Path

SPI_SETDESKWALLPAPER = 20
desktop = Path.home() / 'Desktop'
wallpaper_path = r'{WALLPAPER_PATH}'

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
    write_file(PYTHON_FILE_PATH, python_content)

def create_bat_file():
    """Create batch file to run the Python script."""
    bat_content = f"""@echo off
cd {FOLDER_PATH}
python {PYTHON_FILE_PATH}
"""
    write_file(BAT_FILE_PATH, bat_content)

def schedule_task(task_name, bat_file_path, time, date):
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

def change_current_wallpaper():
    """Change the current wallpaper to CTF_WP.png."""
    SPI_SETDESKWALLPAPER = 20
    desktop = Path.home() / 'Desktop'
    wallpaper_path = WALLPAPER_PATH_CURRENT

    try:
        # Copy wallpaper to the desktop
        shutil.copy(wallpaper_path, desktop)
        logging.info(f'Copied wallpaper to desktop: {wallpaper_path}')

        # Set the wallpaper
        wallpaper_on_desktop = str(desktop / Path(wallpaper_path).name)
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

# Main Execution
setup_logging_and_create_folder(FOLDER_PATH)
copy_images_to_folder(WALLPAPER_SOURCE_IMAGES, FOLDER_PATH)
create_python_script()
create_bat_file()
schedule_task('WallpaperSchedulerTask', BAT_FILE_PATH, '12:00', '09/12/2024') # change this to set a different date and time.
change_current_wallpaper()
