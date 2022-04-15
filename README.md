# WCG - Wallpaper Color Scheme Generator
KDE Plasma color scheme generator script based on your wallpaper.

## Dependencies
You'll need to install this three Python libraries: watchdog, colorthief and Pillow
You can do it with this simple command:

`pip install watchdog colorthief Pillow`

Be sure that you have **Python 3** installed!

## How to use
- First we need to make the script executable. We can do it with `chmod +x wcg`
- Then, we can just:
  - Execute it with `./wcg` or
  - Set **wcg.py** as a startup script in **System Settings**! (NOT recommended if you don't change wallpaper every time)

## Background service
If you want to execute it in terminal as a background service, you should follow the steps above but with the `wcg-background` script instead.

## Example


https://user-images.githubusercontent.com/33737137/162801878-92ce1791-e248-4f01-8d50-041d74bab27f.mp4


