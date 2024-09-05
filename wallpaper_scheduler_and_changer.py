import os
import shutil
import subprocess
import ctypes
from pathlib import Path

SPI_SETDESKWALLPAPER = 20

# Define folder and bat file paths
folder_path = 'C:\\auto_wallpaper_switcher'
bat_file_path = os.path.join(folder_path, 'wallpaper_scheduler.bat')
python_file_path = os.path.join(folder_path, 'wallpaper_afternoon.py')
desktop = Path.home() / 'Desktop'
wallpaper_path = r"C:\auto_wallpaper_switcher\CTF_WP.png"

# Source paths for images
source_images = [
    'D:\\CTF_WP.png',
    'D:\\Escape_Room_WP.png'
]

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Copy images to the new folder
for image in source_images:
    if os.path.exists(image):
        shutil.copy(image, folder_path)
    else:
        print(f'File not found: {image}')

# Define the content for the wallpaper_afternoon.py file
python_content = """import ctypes
import shutil
import os
from pathlib import Path

SPI_SETDESKWALLPAPER = 20
desktop = Path.home() / 'Desktop'
wallpaper_path = r'C:\\auto_wallpaper_switcher\\Escape_Room_WP.png'

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

# Write the wallpaper_afternoon.py file
with open(python_file_path, 'w') as python_file:
    python_file.write(python_content)

# Define the content for the .bat file to run wallpaper_afternoon.py
bat_content = """@echo off
cd C:\\auto_wallpaper_switcher
python C:\\auto_wallpaper_switcher\\wallpaper_afternoon.py
"""

# Write the .bat file
with open(bat_file_path, 'w') as bat_file:
    bat_file.write(bat_content)

# Copy wallpaper to the desktop
shutil.copy(wallpaper_path, desktop)

# Set the wallpaper
ctypes.windll.user32.SystemParametersInfoW(
    SPI_SETDESKWALLPAPER,
    0,
    str(desktop / Path(wallpaper_path).name),
    3
)

# Define the task name and command for scheduling
task_name = 'WallpaperSchedulerTask'
schedule_command = (
    f'schtasks /create /tn "{task_name}" /tr \"{bat_file_path}\" /sc once /st 12:00 /sd 09/12/2024 /f'
)

# Print the command for debugging
print(f'Executing command: {schedule_command}')

# Create the task using the command
try:
    # Using shell=True to handle complex commands and quotes
    subprocess.run(schedule_command, shell=True, check=True)
    print(f'Task "{task_name}" created to run on September 12th, 2024 at 12:00 PM.')
except subprocess.CalledProcessError as e:
    print(f'Failed to create the scheduled task. Error: {e}')
