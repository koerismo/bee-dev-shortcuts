# bee-dev-tool
a tool to make bee packages less painful

### this program may not work 100% of the time.

***

Things required:
- Python 3.7+
- Blender 2.8
- Windows
- Pillow library

# Usage
### Be sure to modify config.json before using.
items needed:
- a texture image (png)
- a 3d model (obj)

Download the Blender 2.8 portable zip from blender.org and place it in `bee_tools/exe/`

Extract Blender so that it follow a structure similar to `/exe/blender-2.82a-windows64/blender.exe`

Open `blender.exe` and install the blender source tools addon. (I pre-downloaded this so you don't have to, it is located in `/exe/`

Modify `bee_tools/config.json` so that it properly reflects your system. Chances are, you will only have to modify the Blender path and your portal 2 path.

that's the entire thing. To use, launch `bee_tools/resources/bee_icon_gen.py` with python 3 and supply it with a png and an obj file.

Examples:

`python3 bee_icon_gen.py "my_image.png" "my_obj.obj"`

`python3 bee_icon_gen.py "my_obj.obj" "my_image.png"`

> You may encounter an error when the program attempts to create `bee_tools/temp` after deleting it. This will not cause any problems if the program is launched without this folder present. It will be created again.

When adding an item, resources will be placed in subfolders named after your package. Make sure your item name is unique. A good practice is to begin the item name with your package name.
