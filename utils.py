import colorsys
import os
from PIL import Image
from colorthief import ColorThief
import time

dir = os.path.dirname(__file__)
darkColorScheme = f"{dir}/Color-scheme/TemplateDark.colors"
lightColorScheme = f"{dir}/Color-scheme/TemplateLight.colors"
darkKonsoleColorScheme = f"{dir}/Konsole/TemplateDark.colorscheme"
lightKonsoleColorScheme = f"{dir}/Konsole/TemplateLight.colorscheme"
konsoleTemplate = f"{dir}/Konsole/Template.profile"
kwinrules = os.path.expanduser("~/.config/kwinrulesrc")
kcolorschemes = os.path.expanduser("~/.local/share/color-schemes")
konsoleDir = os.path.expanduser("~/.local/share/konsole")
config = os.path.expanduser(
    "~/.config/plasma-org.kde.plasma.desktop-appletsrc")


def lighten(color, amount=0.5):
    r = color[0]
    g = color[1]
    b = color[2]

    hslColor = colorsys.rgb_to_hls(r, g, b)

    newR = hslColor[0] if hslColor[0] <= 255 else 255
    newG = 1 - amount * (1 - hslColor[1])
    newB = hslColor[2]

    colorTuple = colorsys.hls_to_rgb(newR, newG, newB)

    colorList = list(colorTuple)
    colorList[:] = [x if x <= 255 else 255 for x in colorList]
    colorTuple = tuple(colorList)

    return f'{",".join(map(str, tuple(map(int, colorTuple))))}'


def setColorScheme(color):
    r = color[0]
    g = color[1]
    b = color[2]

    if (r*0.299 + g*0.587 + b*0.114) > 186:
        return (lightColorScheme, "light")
    else:
        return (darkColorScheme, "dark")


def setKonsoleColorScheme(mode):
    if (mode == "light"):
        return (lightKonsoleColorScheme, konsoleTemplate)
    else:
        return (darkKonsoleColorScheme, konsoleTemplate)


def getWallpaper():
    configFile = open(config, "r")

    time.sleep(0.5)

    isInWallpaper = False
    imagePath = ''

    for line in configFile:
        if "[" in line:
            isInWallpaper = False
        if "[Wallpaper]" in line:
            isInWallpaper = True
        if "Image" in line and isInWallpaper:
            imagePath = line[6:].rstrip().replace('file:/', '')
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
