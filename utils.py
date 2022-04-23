import subprocess
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
    isLight = (r*0.299 + g*0.587 + b*0.114) > 127.5

    if isLight:
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


def generateKonsoleColors(mode, palette):
    colorName = 'WCG'
    colorNameAlt = 'WCG-Alt'
    colorScheme, colorProfile = setKonsoleColorScheme(mode)

    background1 = lighten(palette[0], 1)
    background2 = lighten(palette[0], 1.1)
    background3 = lighten(palette[0], 0.9)
    accent1 = lighten(palette[1], 1)
    accent2 = lighten(palette[1], 1.1)
    accent3 = lighten(palette[1], 0.9)

    # COLORS PALETTE
    colors = (background1, background2, background3)
    colorsAlt = (accent1, accent2, accent3)

    # CREATE DIR
    createDirectoryCommand = f'mkdir -p {konsoleDir}'
    subprocess.Popen(createDirectoryCommand.split(),
                     stdout=subprocess.PIPE)

    # CREATE NORMAL SCHEME
    newColorScheme = f'{konsoleDir}/{colorName}.colorscheme'
    newColorProfile = f'{konsoleDir}/{colorName}.profile'

    subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(),
                     stdout=subprocess.PIPE).wait()
    subprocess.Popen(f'cp {colorProfile} {newColorProfile}'.split(),
                     stdout=subprocess.PIPE).wait()

    # CREATE ALTERNATIVE SCHEME
    newColorSchemeAlt = f'{konsoleDir}/{colorName}-Alt.colorscheme'
    newColorProfileAlt = f'{konsoleDir}/{colorName}-Alt.profile'

    subprocess.Popen(f'cp {colorScheme} {newColorSchemeAlt}'.split(),
                     stdout=subprocess.PIPE).wait()
    subprocess.Popen(f'cp {colorProfile} {newColorProfileAlt}'.split(),
                     stdout=subprocess.PIPE).wait()

    # CREATE NORMAL STYLE FILES
    createKonsoleColorschemeFile(
        newColorScheme, colorName, colors)
    createKonsoleProfileFile(newColorProfile, colorName)

    # CREATE ALTERNATIVE STYLE FILES
    createKonsoleColorschemeFile(
        newColorSchemeAlt, colorName, colorsAlt)
    createKonsoleProfileFile(newColorProfileAlt, colorNameAlt)


def createKonsoleColorschemeFile(newColorScheme, colorName, colors):
    colorSchemeFile = open(newColorScheme, "r")
    colorSchemeLines = colorSchemeFile.readlines()
    colorSchemeFile.close()

    newColorSchemeFile = open(newColorScheme, "w")

    for line in colorSchemeLines:
        if "{BACKGROUND_1}" in line:
            line = line.replace("{BACKGROUND_1}", colors[0])
        if "{BACKGROUND_2}" in line:
            line = line.replace("{BACKGROUND_2}", colors[1])
        if "{BACKGROUND_4}" in line:
            line = line.replace("{BACKGROUND_4}", colors[2])
        if "{NAME}" in line:
            line = line.replace("{NAME}", colorName)
        newColorSchemeFile.write(line)

    newColorSchemeFile.close()


def createKonsoleProfileFile(newColorProfile, colorName):
    colorProfileFile = open(newColorProfile, "r")
    colorProfileLines = colorProfileFile.readlines()
    colorProfileFile.close()

    newColorProfileFile = open(newColorProfile, "w")

    for line in colorProfileLines:
        if "{NAME}" in line:
            line = line.replace("{NAME}", colorName)
        newColorProfileFile.write(line)

    newColorProfileFile.close()
