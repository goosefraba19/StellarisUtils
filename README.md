# StellarisUtils

A collection of scripts that I use to analyze and visualize my Stellaris playthroughs.

## Dependencies

Make sure that Python 3.7 is installed, along with these packages:

- [Pillow](https://pypi.org/project/Pillow/) (5.2.0)
- [numpy](https://pypi.org/project/numpy/) (1.15.0)
- [scipy](https://pypi.org/project/scipy/) (1.1.0)

## How to Make Timelapses

The process I've developed for making timelapses consists of four steps: acquiring the savefiles, converting them, generating the images, and then generating an animation.

#### 1. Acquiring Savefiles

##### copy_autosave_files.py

![](https://i.imgur.com/l20OYKm.png)

This script is run in the background while you are playing Stellaris and periodically checks the entire "save games" folder for new autosave files. It then copies those new files into the saves folder for the project.

There are some values in **settings.json** that you need to verify in order for this script to work. 
 * "stellaris_folder_path" must point to the folder where Stellaris stores all your current data, which contains these folders and files:

![](https://i.imgur.com/Nm5czvU.png)

 * "saves_folder_path" is the folder where all the copied savefiles will end up. You can leave this with the default value.

#### 2. Converting Savefiles



#### 3. Generating Images



#### 4. Generating Animation

I use [GIMP](https://www.gimp.org/) to generate the animations, by loading all the images into the same project as separate layers and then exporting them as a GIF.


