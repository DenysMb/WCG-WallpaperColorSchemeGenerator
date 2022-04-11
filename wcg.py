import subprocess
import os
from utils import getPalette, getWallpaper
from utils import lighten, setColorScheme, kcolorschemes
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def changeWallpaper(imagePath):
    palette = getPalette(imagePath)

    colorTuple = palette[0]
    dominantColor = lighten(palette[0], 1)
    accentColor = lighten(palette[1], 1)
    darkDominantColor = lighten(colorTuple, 0.9)

    createDirectoryCommand = f'mkdir -p {kcolorschemes}'
    subprocess.Popen(createDirectoryCommand.split(),
                    stdout=subprocess.PIPE)

    colorName = 'WSG-Current'

    newColorScheme = f'{kcolorschemes}/{colorName}.colors'
    newColorSchemeAlt = f'{kcolorschemes}/{colorName}-Alt.colors'
    newColorSchemePlain = f'{kcolorschemes}/{colorName}-Plain.colors'

    colorScheme = setColorScheme(colorTuple)

    subprocess.Popen(f'cp {colorScheme} {newColorScheme}'.split(),
                    stdout=subprocess.PIPE).wait()
    subprocess.Popen(
        f'cp {colorScheme} {newColorSchemeAlt}'.split(), stdout=subprocess.PIPE).wait()
    subprocess.Popen(
        f'cp {colorScheme} {newColorSchemePlain}'.split(), stdout=subprocess.PIPE).wait()

    colorSchemeFile = open(newColorScheme, "r")
    colorSchemeLines = colorSchemeFile.readlines()
    colorSchemeFile.close()

    newColorSchemeFile = open(newColorScheme, "w")

    isInSelection = False
    isInView = False

    for line in colorSchemeLines:
        if "[Colors:Selection]" in line:
            isInSelection = True
        if "[Colors:Tooltip]" in line:
            isInSelection = False
        if "[Colors:View]" in line:
            isInView = True
        if "[Colors:Window]" in line:
            isInView = False
        if "Name" in line:
            continue
        if "BackgroundNormal" in line:
            line = f'BackgroundNormal={darkDominantColor if isInView else dominantColor if not isInSelection else accentColor}\n'
        if "BackgroundAlternate" in line:
            line = f'BackgroundAlternate={darkDominantColor if isInView else dominantColor if not isInSelection else accentColor}\n'
        if "DecorationFocus" in line:
            line = f'DecorationFocus={accentColor}\n'
        if "DecorationHover" in line:
            line = f'DecorationHover={accentColor}\n'
        if "activeBackground" in line:
            line = f'activeBackground={dominantColor}\n'
        if "inactiveBackground" in line:
            line = f'inactiveBackground={dominantColor}\n'
        if "[General]" in line:
            line = f'[General]\nName={colorName}\n'
        newColorSchemeFile.write(line)

    newColorSchemeFile.close()

    colorSchemeFileAlt = open(newColorSchemeAlt, "r")
    colorSchemeAltLines = colorSchemeFileAlt.readlines()
    colorSchemeFileAlt.close()

    newColorSchemeFileAlt = open(newColorSchemeAlt, "w")

    isInHeader = False
    isInSelection = False
    isInView = False

    for line in colorSchemeAltLines:
        if "[Colors:Header]" in line:
            isInHeader = True
        if "[Colors:Selection]" in line:
            isInSelection = True
            isInHeader = False
        if "[Colors:Tooltip]" in line:
            isInSelection = False
        if "[Colors:View]" in line:
            isInView = True
        if "[Colors:Window]" in line:
            isInView = False
        if "Name" in line:
            continue
        if "BackgroundNormal" in line:
            line = f'BackgroundNormal={darkDominantColor if isInHeader or isInView else dominantColor if not isInSelection else accentColor}\n'
        if "BackgroundAlternate" in line:
            line = f'BackgroundAlternate={darkDominantColor if isInHeader or isInView else dominantColor if not isInSelection else accentColor}\n'
        if "DecorationFocus" in line:
            line = f'DecorationFocus={accentColor}\n'
        if "DecorationHover" in line:
            line = f'DecorationHover={accentColor}\n'
        if "activeBackground" in line:
            line = f'activeBackground={darkDominantColor}\n'
        if "inactiveBackground" in line:
            line = f'inactiveBackground={darkDominantColor}\n'
        if "[General]" in line:
            line = f'[General]\nName={colorName}-Alt\n'
        newColorSchemeFileAlt.write(line)

    newColorSchemeFileAlt.close()

    colorSchemeFilePlain = open(newColorSchemePlain, "r")
    colorSchemePlainLines = colorSchemeFilePlain.readlines()
    colorSchemeFilePlain.close()

    newColorSchemeFilePlain = open(newColorSchemePlain, "w")

    isInSelection = False

    for line in colorSchemePlainLines:
        if "[Colors:Selection]" in line:
            isInSelection = True
        if "[Colors:Tooltip]" in line:
            isInSelection = False
        if "Name" in line:
            continue
        if "BackgroundNormal" in line:
            line = f'BackgroundNormal={darkDominantColor if isInView else dominantColor if not isInSelection else accentColor}\n'
        if "BackgroundAlternate" in line:
            line = f'BackgroundAlternate={darkDominantColor if isInView else dominantColor if not isInSelection else accentColor}\n'
        if "DecorationFocus" in line:
            line = f'DecorationFocus={accentColor}\n'
        if "DecorationHover" in line:
            line = f'DecorationHover={accentColor}\n'
        if "activeBackground" in line:
            line = f'activeBackground={dominantColor}\n'
        if "inactiveBackground" in line:
            line = f'inactiveBackground={dominantColor}\n'
        if "[General]" in line:
            line = f'[General]\nName={colorName}-Plain\n'
        newColorSchemeFilePlain.write(line)

    newColorSchemeFilePlain.close()

    subprocess.Popen(f'plasma-apply-colorscheme BreezeDark'.split(),
                    stdout=subprocess.PIPE).wait()
    subprocess.Popen(f'plasma-apply-colorscheme {colorName}'.split(),
                    stdout=subprocess.PIPE).wait()


wallpaperConfigFile = os.path.expanduser(
    "~/.config/plasma-org.kde.plasma.desktop-appletsrc")
oldWallpaper = getWallpaper()

event_handler = LoggingEventHandler()
observer = Observer()
observer.schedule(event_handler, wallpaperConfigFile, recursive=True)
observer.start()

try:
    while True:
        newWallpaper = getWallpaper()

        if (newWallpaper != oldWallpaper):
            oldWallpaper = newWallpaper
            changeWallpaper(newWallpaper)
except KeyboardInterrupt:
    observer.stop()
observer.join()
