import colorsys
import subprocess
import os
from PIL import Image
from colorthief import ColorThief

darkColorScheme = "/usr/share/color-schemes/BreezeDark.colors"
lightColorScheme = "/usr/share/color-schemes/BreezeLight.colors"
kwinrules = os.path.expanduser("~/.config/kwinrulesrc")
kcolorschemes = os.path.expanduser("~/.local/share/color-schemes")
config = os.path.expanduser(
    "~/.config/plasma-org.kde.plasma.desktop-appletsrc")


def lighten(color, amount=0.5):
    r = color[0]
    g = color[1]
    b = color[2]

    hslColor = colorsys.rgb_to_hls(r, g, b)
    newColor = colorsys.hls_to_rgb(
        hslColor[0], 1 - amount * (1 - hslColor[1]), hslColor[2])

    return f'{",".join(map(str, tuple(map(int, newColor))))}'


def setColorScheme(color):
    r = color[0]
    g = color[1]
    b = color[2]

    if (r*0.299 + g*0.587 + b*0.114) > 186:
        return lightColorScheme
    else:
        return darkColorScheme


def getWallpaper():
    configFile = open(config, "r")

    isInWallpaper = False
    imagePath = ''

    for line in configFile:
        if "[" in line:
            isInWallpaper = False
        if "[Wallpaper]" in line:
            isInWallpaper = True
        if "Image" in line and isInWallpaper:
            imagePath = line[6:].rstrip()
            break

    configFile.close()

    return imagePath


def getPalette(imagePath):
    imageFile = Image.open(imagePath).resize((150, 150))
    imageExtension = imagePath.split('.')[-1]

    resizedImageName = f'/tmp/resized.{imageExtension}'
    imageFile.save(resizedImageName)
    resizedImagePath = os.path.expanduser(resizedImageName)

    colorThief = ColorThief(resizedImagePath)
    palette = colorThief.get_palette(color_count=2)

    return palette
