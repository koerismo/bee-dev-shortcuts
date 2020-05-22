print("Starting Bee Item Helper...")
error_persist_message = "If this issue persists, please submit an issue.\n\n"
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
import gen_qc
from pathlib import Path
import shutil

#set vars
icon = ""
texture = ""
model = ""
pkg_struct_req = [
    "/info.txt",
    "/resources/models/props_map_editor/",
    "/resources/models/puzzlemaker/"
]

def reformatError(er):
    return str("\n".join(map(str,str(er).split("\\n"))))
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
    vprocess = subprocess.run([vtfcmd_path, '-file',bt_dir+"\\temp\\icon_large.png",'-output',bt_dir+"\\temp"],stdout=subprocess.PIPE)
    if (not os.path.isfile(bt_dir+"\\temp\\icon_large.vtf")):
        logging.exception(f"\n\nVTFCmd failed to run!\nVTFCmd path:{vtfcmd_path}\nOutput message:\n\n{reformatError(vprocess.stdout)}\n\n{error_persist_message}")
        exit()
    lbar.settext("[icons] finished!")
    lbar.setbar(100)
    lbar.end()

#get bee_tools dir
bt_dir = os.path.abspath(__file__+"/../..")
bset(50,"loading configuration...")
#load config
bt_config = json.loads(open(bt_dir+"/config.json","r").read())
blender_path = [bt_dir+bt_config["blender exe"] if bt_config["blender relative"] else bt_config["blender exe"]][0]
vtfcmd_path = [bt_dir+bt_config["vtfcmd exe"] if bt_config["vtfcmd relative"] else bt_config["vtfcmd exe"]][0]
pkg_name = "_".join((os.path.split(bt_config["package root"])[-1]).lower().split(" "))
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
    logging.exception(f"\n\nBlender failed to run!\nBlender path:{blender_path}\nError message:\n\n{e}\n\n{error_persist_message}")
    exit()
#insert test launch here
bset(80,"verifying VTFCmd...")
try:
    vresult = subprocess.run([bt_dir+bt_config["vtfcmd exe"], '-help'], stdout=subprocess.PIPE)
except Exception as e:
    lbar.end()
    logging.exception(f"\n\nVTFCmd failed to run!\nVTFCmd path:{vtfcmd_path}\nError message:\n\n{e}\n\n{error_persist_message}")
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
item_name = input("\nitem name: ")
lbar.begin()
lbar.setbar(0)
if not (model == ""):
    lbar.settext("processing model...")
    try:
        bprocess = subprocess.run([blender_path,'-b',bt_dir+'/resources/default.blend',
                                   '-x','0',
                                   '--python-exit-code','1',
                                   '--python',bt_dir+bt_config["blender script"],
                                   '--',
                                   '-mi',model,
                                   '-tx',texture,
                                   '-mo',bt_dir+"\\temp",
                                   '-ep',bt_config["portal 2 folder"]+"\\bin\\",
                                   '-mn',item_name+"_mat.vmt"
                                   ],stdout=subprocess.PIPE)
        print(bprocess.stdout)
    except: #'-f','0','-o',bt_dir+'/temp/icon_rendered.png','--debug-python',
        bset(0,"an error occurred in blender!")
        lbar.end()
        raise(Exception('\n\nAn error occurred in Blender.\nError:\n\n'+reformatError(bprocess.stdout)+'\n\n'+error_persist_message))
    if (bprocess.returncode != 0):
        bset(0,"an error occurred in blender!")
        lbar.end()
        raise(Exception('\n\nAn error occurred in Blender.\nError:\n\n'+reformatError(bprocess.stdout)+'\n\n'+error_persist_message))
    lbar.setbar(100)
    lbar.end()
lbar.begin()
lbar.settext("processing icons...")
try:
    if (icon != ""):
        saveIcon(icon)
    else:
        saveIcon(bt_dir+"\\temp\\icon_rendered.png")
except Exception as e:
    lbar.end()
    logging.exception('\n\nAn error occurred during image processing.\nError message:\n\n'+str(e)+'\n\n'+error_persist_message)
    exit()
lbar.end()

#copy texture to temp and rename
subprocess.run(f'copy {texture} {bt_dir}\\temp\\item_texture.png',shell=True)
vprocess = subprocess.run([vtfcmd_path, '-file',bt_dir+"\\temp\\item_texture.png",'-output',bt_dir+"\\temp\\"])
if (not os.path.isfile(bt_dir+"\\temp\\icon_large.vtf")):
    logging.exception(f"\n\nVTFCmd failed to run!\nVTFCmd path:{vtfcmd_path}\nOutput message:\n\n{reformatError(vprocess.stdout)}\n\n{error_persist_message}")
    exit()
#copy converted vtf to package directory
print("\n\ncopying vtf model texture to package...\n")
Path(f'{bt_config["package root"]}\\resources\\materials\\BEE2\models\\props_map_editor\\{pkg_name}').mkdir(parents=True, exist_ok=True)
subprocess.run(['copy',
                f'{bt_dir}\\temp\\item_texture.vtf',
                f'{bt_config["package root"]}\\resources\\materials\\BEE2\models\\props_map_editor\\{pkg_name}\\{item_name}_mat.vtf'],shell=True)

#create vmt
print("\n\ncreating vmt in package...\n")
Path(bt_config["package root"]+f"\\resources\\materials\\BEE2\models\\props_map_editor\\{pkg_name}").mkdir(parents=True, exist_ok=True)
gen_qc.saveVMT(
    f"BEE2\models\props_map_editor\{pkg_name}\{item_name}_mat.vtf",
    bt_config["package root"]+f"\\resources\\materials\\BEE2\models\\props_map_editor\\{pkg_name}\\{item_name}_mat.vmt"
    )
#convert texture to vtf, create vmt, and place into directory
#vtf directory: "resources\materials\BEE2\models\props_map_editor\{pkg_name}\{item_name}_mat.vtf"

#generate qc
qc_properties = {
    "export_path":bt_config["temp model folder"]+"\\temp.mdl",
    "cd_mats":"BEE2\\models\\props_map_editor\\"+pkg_name.lower()+"\\",
    "smd_path":bt_dir+"\\temp\\Collection.smd"
    #"export_path":bt_config["portal 2 folder"]+"\\portal2\\models"+bt_config["temp model folder"]
}
gen_qc.saveQC(qc_properties,bt_dir+"\\temp\\Collection.qc")
print("\n\ncompiling model...\n")
#compile model
try:
    stprocess = subprocess.run([f'{bt_config["portal 2 folder"]}\\bin\\studiomdl.exe',
                                f'-game',f'{bt_config["portal 2 folder"]}\\portal2',
                                f'{bt_dir}\\temp\\Collection.qc'
                                   ],stdout=subprocess.PIPE)
    if (stprocess.returncode != 0):
        print(stprocess.stdout)
        exit()
except Exception as e:
    logging.exception('\n\nAn error occurred during model compilation.\nError message:\n\n'+str(e)+'\n\n'+error_persist_message)

#copy icons to package
print("\n\ncopying icons to package folder...\n")

#copy bee2 icon
Path(bt_config["package root"]+f'\\resources\\BEE2\\items\\{pkg_name}').mkdir(parents=True, exist_ok=True)
shutil.copy(bt_dir+"\\temp\\icon_small.png",
bt_config["package root"]+f'\\resources\\BEE2\\items\\{pkg_name}\\{item_name}.png')

#copy ingame icon
Path(bt_config["package root"]+f'\\resources\\materials\\models\\props_map_editor\\palette\\bee2\\{pkg_name}').mkdir(parents=True, exist_ok=True)
shutil.copy(bt_dir+"\\temp\\icon_large.vtf",
bt_config["package root"]+f'\\resources\\materials\\models\\props_map_editor\\palette\\bee2\\{pkg_name}\\{item_name}.vtf')
    
#copy model folder to temp
print("\n\ncopying compiled models to temp folder...\n")
shutil.copytree( #yep, i have to use this.
    f'{bt_config["portal 2 folder"]}\\portal2\\models{bt_config["temp model folder"]}',
    f'{bt_dir}\\temp\\compiled'
    )
print("\n\ncopying models from temp to package...\n")
#rename all files
mp_path = os.path.abspath(f'{bt_dir}\\temp\\compiled')+"\\"
Path(bt_config["package root"]+f"\\resources\\models\\props_map_editor\\{pkg_name}").mkdir(parents=True, exist_ok=True)
for x in os.listdir(mp_path):
    print(f"copying {mp_path+x}...")
    shutil.copy(mp_path+x,
f'{bt_config["package root"]}\\resources\\models\\props_map_editor\\{pkg_name}\\{x.replace("temp",item_name)}')

print("\n\nCleaning up...")
shutil.rmtree(bt_dir+"\\temp\\")
os.makedirs(bt_dir+"\\temp\\")
shutil.rmtree(f'{bt_config["portal 2 folder"]}\\portal2\\models{bt_config["temp model folder"]}')

print("\n\nFinished processing! All resources exported to package.\n")
input("")
