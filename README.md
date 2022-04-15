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
  - Set **wcg.py** as a startup script in **System Settings**!

## Background service
If you want to execute it in terminal as a background service, you should follow the steps above but with the `wcg-background` script instead.


## Example

https://user-images.githubusercontent.com/33737137/162801878-92ce1791-e248-4f01-8d50-041d74bab27f.mp4


## WSG Modes
WSG have 4 different modes, they are:

### WSG
Mode that works like Breeze themes (with active and inactive header color)

![WSG-Normal](https://user-images.githubusercontent.com/33737137/163511221-4625955f-4f57-44a7-ad74-b70036256bc6.gif)
![LightWSG](https://user-images.githubusercontent.com/33737137/163511864-74573219-f64d-481b-87dc-b8cd73b6006b.gif)


### WSG-DarkHeader
Mode that have a darker header always active

![WSG-DarkHeader](https://user-images.githubusercontent.com/33737137/163511295-d5d107df-03bd-47eb-b9b8-3d43327b8527.gif)
![LightWSG-DarkHeader](https://user-images.githubusercontent.com/33737137/163511873-e09faf42-7550-4dcb-a56c-d5dbefd170be.gif)


### WSG-NoHeader
Mode that the header doesn't have a different color

![WSG-NoHeader](https://user-images.githubusercontent.com/33737137/163511355-440fe8d3-66ff-400d-a89a-1d0c36615dbb.gif)
![LightWSG-NoHeader](https://user-images.githubusercontent.com/33737137/163511878-36ae51fb-c507-41c3-8aeb-02e7e59518f9.gif)


### WSG-Plain
Mode that everything is of the same color (except from the accent colors)

![WSG-Plain](https://user-images.githubusercontent.com/33737137/163511417-57baa4aa-4069-4cb1-aeea-6ee5a9f1a15d.gif)
![LightWSG-Plain](https://user-images.githubusercontent.com/33737137/163511890-7cc4c46e-e7fe-401c-95c8-1b5fc1fa371d.gif)

## Check too
You can check too my others two scripts:
- [CSG - Color Scheme Generator](https://github.com/DenysMb/CSG-ColorSchemeGenerator): With this script you can easily generate any color-scheme by using a color picker!
- [TKP - Tile Color Picker](https://github.com/DenysMb/TKP-TileColorPicker): With this script you can set the header/tile color of a window to match with their main window color. This is a Python version of the [TKP script](https://github.com/siggsy/Tkp) from [@siggsy](https://github.com/siggsy)
