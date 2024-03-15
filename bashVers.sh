#!/bin/bash


image_1="/mnt/d/ConcealCTFBackground.png"
image_2="/mnt/d/SRNLEscapeRoomBackground.png"


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
