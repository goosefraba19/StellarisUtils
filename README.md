# StellarisUtils

A collection of scripts that I use to analyze and visualize my Stellaris playthroughs.

## Dependencies

Make sure that Python 3.7 is installed, along with these packages:

- [Pillow](https://pypi.org/project/Pillow/) (5.2.0)
- [numpy](https://pypi.org/project/numpy/) (1.15.0)
- [scipy](https://pypi.org/project/scipy/) (1.1.0)

## How to Make Timelapses

The process I've developed for making timelapses consists of four steps: acquiring the savefiles, converting them, rendering the images, and then generating an animation.

### 1. Acquiring Savefiles

##### copy_autosave_files.py

![](https://i.imgur.com/OJYazdU.png)

This script is run in the background while you are playing Stellaris and periodically checks the entire "save games" folder for new autosave files. It then copies those new files into the saves folder for the project. 

There are some values in **settings.json** that you need to verify in order for this script to work. 
 * "stellaris_folder_path" must point to the folder where Stellaris stores all your current data, which contains these folders and files:

![](https://i.imgur.com/foimXIN.png)

 * "saves_folder_path" is the folder where all the copied savefiles will end up. You can leave this with the default value.

### 2. Converting Savefiles

##### convert_saves_to_json.py

![](https://i.imgur.com/GdfS85y.png)

This script converts the savefiles for a specific game from their native format into a zipped JSON file. This is done to speed up the later steps, since Python's JSON parser is much quicker than my own savefile parser. When run, the script ignores savefiles that have already been converted.

**NOTE**: This step will probably take a long time to complete!

The key values in **settings.json** that you should verify are:

* "current" is the name of the subfolder on which the script will operate. The script will look for new savefiles in "&lt;saves_folder_path&gt;/&lt;current&gt;" and place the converted files in "&lt;json_folder_path&gt;/&lt;current&gt;".

* "saves_folder_path" should still be the folder where all the copied savefiles ended up from the previous step.

* "json_folder_path" is the folder where the converted files will end up. You can leave this with the default value.


### 3. Rendering Images

**render_latest.py** & **render_all.py**

There are two scripts for rendering images. Use **render_latest.py** to evaluate the current settings and adjust accordingly, and once you're happy run **render_all.py**. All the images are saved in the output folder.

The key values in **settings.json** that you should focus on are:

* "current" should still be the same from the previous step.

* "output_folder_path" is where all the rendered images are saved. You can leave this with the default value.

* "render" holds all the details used to produce the images.

**settings.json: "render"**

While working with **render_latest.py**, expect to modify the "render" section multiple times before finding the correct settings. Adjust the "image" subsection's "size", "center", and "scale" values so that the galaxy fits nicely inside the image. If the script is reporting missing colors, add them to the "color" subsection and feel free to let me know they're missing. 

The "steps" subsection describes the rendering steps. The default settings renders regions, hyperlanes, pops, and then the date in the upper-left corner. Each step also contains settings controlling how they operate.

The regions step will most likely need adjustment before you render all the images. It uses a Voronoi diagram to determine the zone around a system, and this works well for almost all of the systems. However, it doesn't work well for systems on the outer rim, inner rim, and in the L-cluster.

![](https://i.imgur.com/hdOVHXq.png)

To fix this issue, I've added some rings marking the boundaries in the "voronoi_rings" list in the regions step settings. However, these boundaries might not work so well for your savefile. 

First, set the "debug" setting to true, and then points will be included in the image for each ring specified. You'll want three rings: one along the inner rim, one along the outer rim, and one surrounding the L-cluster. 

Each ring consists of 4 values: 
 
* x - horizontal position
* y - vertical position
* r - radius of the ring
* s - (step) the angle between each point generated

The final result should look something like this:

![](https://i.imgur.com/LkDvaAR.png)

Set "debug" to false to get rid of the ring points, and then go ahead and run **render_all.py** to generate an image for every converted savefile in the current game's json folder.


### 4. Generating Animation

I use [GIMP](https://www.gimp.org/) to generate the animations, by loading all the images into the same project as separate layers and then exporting them as a GIF.
