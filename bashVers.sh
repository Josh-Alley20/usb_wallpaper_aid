#!/bin/bash

# put image file paths from D:\ drive
image_1="D:\image_1"
image_2="D:\image_2"


destination="$HOME/Desktop"

# Wait for user input before proceeding
read -p "[i] Press Enter to set wallpaper"

if [ -f "$image_1" ]; then
    cp "$image_1" "$destination"
    cp "$image_2" "$destination"
else
    echo "[i] File $image_1 not found\a\a\a\a"
    exit 1
fi

echo "[i] Wallpaper set successfully [i]"
