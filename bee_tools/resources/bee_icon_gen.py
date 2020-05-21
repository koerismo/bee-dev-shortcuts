print("Starting Bee Item Helper...")
error_persist_message = "If this issue persists, please submit an issue."
#load resources
import loadingbar, logging #lmao we have to preload the loading bar
lbar = loadingbar.bar(15)
lbar.begin()
lbar.settext("Loading modules...")
def bset(br,txt):
    lbar.setbar(br)
    lbar.settext(txt)
    
import subprocess
lbar.setbar(8)
import sys
lbar.setbar(14)
import json
lbar.setbar(20)
import os
lbar.setbar(26)
from PIL import Image
lbar.setbar(40)

#set vars
icon = ""
texture = ""
model = ""
pkg_struct_req = [
    "/info.txt",
    "/resources/models/props_map_editor/",
    "/resources/models/puzzlemaker/"
]

def saveIcon(icon):
    lbar.setbar(0)
    img_icon = Image.open(icon)
    lbar.setbar(14)
    lbar.settext("[icons] resizing...")
    img_icon_small = img_icon.resize((64,64), Image.ANTIALIAS)
    lbar.setbar(28)
    img_icon_large = img_icon.resize((256,256), Image.ANTIALIAS)
    lbar.setbar(42)
    lbar.settext("[icons] saving pngs...")
    img_icon_small.save(bt_dir+'/temp/icon_small.png')
    lbar.setbar(56)
    img_icon_large.save(bt_dir+'/temp/icon_large.png')
    lbar.setbar(70)
    lbar.settext("[icons] converting to vtf...")
    subprocess.run(['"'+vtfcmd_path+'"', '-input '+bt_dir+"/temp/icon_large.png",'-output '+bt_dir+"/temp/icon_vtf"])
    lbar.settext("[icons] finished!")
    lbar.setbar(100)

#get bee_tools dir
bt_dir = os.path.abspath(__file__+"/../..")
bset(50,"loading configuration...")
#load config
bt_config = json.loads(open(bt_dir+"/config.json","r").read())
blender_path = [bt_dir+bt_config["blender exe"] if bt_config["blender relative"] else bt_config["blender exe"]][0]
vtfcmd_path = [bt_dir+bt_config["vtfcmd exe"] if bt_config["vtfcmd relative"] else bt_config["vtfcmd exe"]][0]

bset(60,"verifying Package structure...")
pkg_struct_err = [x for x in pkg_struct_req if not os.path.exists(bt_config["package root"]+x)]
if len(pkg_struct_err) > 0:
    lbar.end()
    raise(Exception("\n\nPackage structure failed to validate!\n\nMissing items:\n- %s\n" % str('\n- '.join([bt_config["package root"]+x for x in pkg_struct_err])) ))
bset(70,"verifying Blender...")
try:
    bresult = subprocess.run([blender_path, '--version','--background'], stdout=subprocess.PIPE)
except Exception as e:
    lbar.end()
    logging.error(f"\n\nBlender failed to run!\nBlender path:{blender_path}\nError message:\n\n{e}\n\n{error_persist_message}")
    exit()
#insert test launch here
bset(80,"verifying VTFCmd...")
try:
    vresult = subprocess.run([bt_dir+bt_config["vtfcmd exe"], '-help'], stdout=subprocess.PIPE)
except Exception as e:
    lbar.end()
    logging.error(f"\n\nVTFCmd failed to run!\nVTFCmd path:{vtfcmd_path}\nError message:\n\n{e}\n\n{error_persist_message}")
    exit()
bset(100,"setup completed!")
lbar.setbar(100)
lbar.end()
for i in sys.argv:
    if not (os.path.isfile(i)):
        continue;
    if (i.endswith("icon.png") or i.endswith("icon.jpg")):
        icon = i
    if (i.endswith("texture.png") or i.endswith("texture.jpg")):
        texture = i
    if (i.endswith(".obj") or i.endswith(".obj")):
        model = i
if (texture == ""): #if there is no icon, treat any image as an texture
    for i in sys.argv:
        if (i.endswith(".png") or i.endswith(".jpg")):
            print("No icon detected! Inferring as texture...")
            texture = i
            break
if (model == ""):
    if (icon == "" and texture == ""):
        #print(sys.argv)
        logging.warn("Nothing to process! Aborting...")
        exit()
    else:
        icon = texture #transfer default to icon if there is no model
        print("No model detected. Skipping...")
else:
    if (icon == "" and texture == ""):
        logging.warn("Your model is missing textures! Aborting...")
        exit()
print(f"Data:\n   icon:{icon}\n   texture:{texture}\n   model:{model}\n")
lbar.begin()
lbar.setbar(0)
if not (model == ""):
    lbar.settext("processing model...")
    try:
        bprocess = subprocess.run([blender_path,'-b',bt_dir+'/resources/default.blend','-o',bt_dir+'/temp/icon_rendered.png','-x','0','--python',bt_dir+bt_config["blender script"],'--','-mi',model],stdout=subprocess.PIPE)
    except:
        bset(0,"an error occurred in blender!")
        lbar.end()
        raise(Exception('\n\nAn error occurred in Blender.\nError:\n\n'+str("\n".join(map(str,str(bprocess.stdout).split("\\n"))))+'\n\n'+error_persist_message))
    if (bprocess.returncode == 1):
        bset(0,"an error occurred in blender!")
        lbar.end()
        raise(Exception('\n\nAn error occurred in Blender.\nError:\n\n'+str("\n".join(map(str,str(bprocess.stdout).split("\\n"))))+'\n\n'+error_persist_message))
    lbar.setbar(100)
    lbar.end()
lbar.begin()
lbar.settext("processing images...")
try:
    if (icon != ""):
        lbar.settext("generating images...")
        saveIcon(icon)
    else:
        saveIcon(bt_dir+"\\temp\\icon_rendered.png")
except Exception as e:
    lbar.end()
    logging.error('\n\nAn error occurred during image processing.\nError message:\n\n'+str(e)+'\n\n'+error_persist_message)
    exit()
lbar.end()
#input("")
#bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), rotation=(0.872665, 0, 0))
