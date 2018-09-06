# StellarisUtils

A collection of scripts that I use to analyze and visualize my Stellaris playthroughs.

Here's an [example timelapse](https://i.imgur.com/NCAWqlG.gifv) made using this project.



## Dependencies

These scripts are to be run in Python 3.7, and depend on these packages:

- [Pillow](https://pypi.org/project/Pillow/) (5.2.0)
- [numpy](https://pypi.org/project/numpy/) (1.15.0)
- [scipy](https://pypi.org/project/scipy/) (1.1.0)

You can ensure these packages are installed by running "python setup.py install" in the project's folder.

## How to Make Timelapses

The process I've developed for making timelapses consists of four steps: acquiring the savefiles, converting them, rendering the images, and then generating an animation.

### 1. Acquiring Savefiles

##### copy_autosave_files.py

![](https://i.imgur.com/OJYazdU.png)

This script should be run in the background while you play Stellaris and periodically checks the entire "save games" folder for new autosave files and updated ironman files. The script copies these new files into the "data" folder for the project. 

In order for this script to work, you need to set a value in **settings.json**. The property *stellaris_folder_path* must point to the folder where Stellaris stores all your data. On Windows, it should be "C:\\Users\\&lt;USERNAME&gt;\\Documents\\Paradox Interactive\\Stellaris", and should contain these folders and files:

![](https://i.imgur.com/foimXIN.png)



### 2. Converting Savefiles

##### convert_saves_to_json.py

![](https://i.imgur.com/GdfS85y.png)

This script converts the savefiles for a specific game from their native format into a zipped JSON file. This is done to speed up the later steps, since Python's JSON parser is much quicker than my own savefile parser. When run, the script ignores savefiles that have already been converted.

**NOTE**: This step will take a long time to complete!

This script relies on the *current* property in **settings.json** to determine which savefiles to convert. Make sure the *current* property has the correct value for the game you are converting, i.e. if you want to covert all the savefiles in "data\\primesequence_-499848856\\saves", then *current* should have the value "primesequence_-499848856".

With the default settings, the converted savefiles will end up in a "json" folder in the current game's folder, i.e. "data\\primesequence_-499848856\\json".



### 3. Rendering Images

**render_latest.py** & **render_all.py**

There are two scripts for rendering images. Use **render_latest.py** to evaluate the current settings and adjust accordingly, and once you're happy run **render_all.py**. All the images are saved in an "output" folder in the current game's folder.

As with the previous step, ensure that the *current* property in **settings.json** has the correct value before running these scripts.

In **settings.json**, the *render* property controls the rendering process. It specifies the image size and scale, the rendering steps, and color configurations. The only settings you will need to tweak are the image size, center, and scale. Adjust the settings, running **render_latest.py** after each change, and evaluate the result in the "output" folder. If the script is reporting missing colors, add them to the *color* list in *render* and feel free to let me know they're missing. Once you're satisfied with the latest image, go ahead and run **render_all.py** to generate an image for every converted savefile.



### 4. Generating Animation

I use [GIMP](https://www.gimp.org/) to generate the animations, by loading all the images into the same project as separate layers and then exporting them as a GIF.
