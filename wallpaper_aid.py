from ctypes import windll
import os
from pathlib import Path
import shutil
import ctypes
from datetime import datetime
import sys

# PUBLIC VERSION (file names redacted for privacy)

# NOTE
# Python 3.8 
# (older version since its the version on our laptops)


class Configs:
    WALLPAPER = 20
    UPDATE_VAL = 0x01
    SEND_CHNG = 0x02


class Images:
    def __init__(self, img_paths: list, output_dir:str) -> None:
        self.images = img_paths
        self.destination = output_dir
    

    def update_clause(self, a_day, a_month):
        today = datetime.now()
        return today.day == a_day and today.month == a_month
            
            
    def guard_clause(self):
        if not os.path.exists(self.destination):
            print(f"[i] Destination Directory { self.destination } was not found and cannot be moved... [i]\a\a\a\a")
            return False
        
        if any(not os.path.exists(img) for img in self.images):
            print(f"[i] A File in the list of images was not found and cannot be moved... [i]\a\a\a\a")
            return False
        
        return True

    def copy_files(self):
        if not self.images:
            print(f"[i] No files were found to copy... [i]\a\a\a\a")
            return
        
        for img in self.images:
            shutil.copy2(img, self.destination)
            print(f"[+] File { img } was copied to { self.destination } successfully... [+]")
            
    def set_wallpaper(self, img_file_name, SETTINGS: Configs) -> None:
        wallpaper_path = str( self.destination.joinpath(img_file_name) )
        return windll.user32.SystemParametersInfoW(SETTINGS.WALLPAPER, 0, wallpaper_path, SETTINGS.UPDATE_VAL | SETTINGS.SEND_CHNG)
    
    # debug info for obj instance
    def __str__(self) -> str:
        return f"< INSTANCE INFO >\nImages: { self.images }\nDrive: { self.disk }"
    


    
    
def main() -> None:
    
    
    # put file paths here (the ones we used for the rentals)
    example_1 = r"D:\example.png"      
    example_2 = r"D:\example2.png"
    
    # prog objs    
    CONF = Configs() 
    data = Images()
    
    # script data set
    # Add the File Name of the images to the list
    data.images = [ 
        example_1,
        example_2 
    ] 
    data.destination = Path(Path.home() / "Desktop") # output directory for files
    wallpaper_file_name = "a_wallpaper.png" # the file name of the wallpaper
    update_file_name = "a_different_wallpaper.png" # the file name of the wallpaper to change the day after event starts 
    
    # sanity check
    if not data.guard_clause():
        print("[i] Please update the data in the script... [i]\a\a\a\a")
        sys.exit()
        
    input("[i] Press < Enter > to run the script  [i]]")
    data.copy_files()
    if data.update_clause(1, 1): # change the date to the day after the event starts
        print("[+] Update condition met... [+]")
        data.set_wallpaper(update_file_name, CONF)
        return    
        
    result = data.set_wallpaper(wallpaper_file_name, CONF)
    if result:
        print("[+] Wallpaper set successfully, closing script... [+]")
        print("[!] Failed to set wallpaper, enter 'y' to retry or anything else to quit... \a\a\a\a\a\a")
        sys.exit()
        
    error_dial = input("[!] Changes failed and an error occured, enter 'y' to retry or anything else to quit...")
    if error_dial.lower() == "y":
        main()

if __name__ == "__main__":
    main()