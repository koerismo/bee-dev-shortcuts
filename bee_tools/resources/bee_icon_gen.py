print("Starting Bee Item Helper...")

#load resources
import loadingbar #lmao we have to preload the loading bar
lbar = loadingbar.bar(15)
lbar.begin()
lbar.settext("Loading modules...")
def bset(br,txt):
    lbar.setbar(br)
    lbar.settext(txt)
    
import subprocess
lbar.setbar(10)
import sys
lbar.setbar(20)
import json
lbar.setbar(30)
import os
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
    img_icon = Image.open(icon)
    img_icon_small = img_icon.resize((64,64), Image.ANTIALIAS)
    img_icon_large = img_icon.resize((256,256), Image.ANTIALIAS)
    img_icon_small.save(bt_dir+'/temp/icon_small.png')
    img_icon_large.save(bt_dir+'/temp/icon_large.png')
    subprocess.run(['"'+vtfcmd_path+'"', '-input '+bt_dir+"/temp/icon_large.png",'-output '+bt_dir+"/temp/icon_vtf"])

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
    bresult = subprocess.run(['"'+blender_path+'"', '--version','--background'], stdout=subprocess.PIPE)
except:
    lbar.end()
    raise(Exception(f"\n\nBlender failed to run!\nPlease check config.json to check for any misspellings.\nBlender path:{blender_path}"))
#insert test launch here
bset(80,"verifying VTFCmd...")
try:
    vresult = subprocess.run([bt_dir+bt_config["vtfcmd exe"], '-help'], stdout=subprocess.PIPE)
except:
    lbar.end()
    raise(Exception(f"\n\nVTFCmd failed to run!\nPlease check config.json to check for any misspellings.\nVTFCmd path:{vtfcmd_path}"))
bset(100,"setup completed!")
lbar.setbar(100)
lbar.end()
for i in sys.argv:
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
        print("Nothing to process! Aborting...")
        exit()
    else:
        icon = texture #transfer default to icon if there is no model
        print("No model detected. Skipping...")
else:
    if (icon == "" and texture == ""):
        print("Your model is missing textures! Aborting...")
        exit()
print(f"Data:\n   icon:{icon}\n   texture:{texture}\n   model:{model}\n")
lbar.begin()
lbar.setbar(0)
if not (model == ""):
    lbar.settext("processing model...")
    bprocess = subprocess.run([blender_path, '--python '+bt_dir+bt_config["blender script"],'--background','-mi "'+model+'"','-r '+bt_dir+"/temp/icon_rendered.png"],stdout=subprocess.PIPE)
    lbar.setbar(100)
    print(bprocess.stdout)
if (icon != ""):
    lbar.settext("generating images...")
    saveIcon(icon)
else:
    saveIcon(bt_dir+"/temp/icon_rendered.png")
#input("")
#bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), rotation=(0.872665, 0, 0))
