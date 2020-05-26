# bee-dev-tool

a tool to make bee packages less painful

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

Run `model_utility.py` to use.

## Arguments

#### `model_utility.py [-h] -mdl -tex -name [-skmat] [-sicon] [-scomp] [-matdir] [-mdldir]`


`  -h, --help`
  
show this help message and exit


`  -mdl, --model-in`
  
OBJ model to be processed.


`  -tex, --texture-in`
  
PNG texture to be processed.


`  -name, --item-name`
  
The prefix that will be assigned to all relevant files.


`  -skmat, --skip-mat`
  
Skip generating materials.


`  -sicon, --skip-icon`
  
Skip generating icon.


`  -scomp, --skip-compile`
  
Skip model compilation.


`  -matdir, --mat-override`
  
Override materials.

Example: `-matdir 'props_map_editor\\my_material.vmt'`


  -mdldir, --model-override
  
Override model.

Example: `-mldir 'props_map_editor\\my_model.mdl'`

***

When adding an item, resources will be placed in subfolders named after your package. Make sure your item name is unique. A good practice is to begin the item name with your name.
