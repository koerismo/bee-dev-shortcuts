try:
    activity = "loading" #cool new crash system
    print("BEE DEVELOPER TOOL V2 BY BAGUETTERY\n\n")
    import loadingbar, subprocess, sys, json, os, gen_qc, shutil, argparse
    from PIL import Image
    from pathlib import Path

    #--------- PARSE ARGUMENTS ---------#

    activity = "parsing arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('-mdl','--model-in', help='OBJ model to be processed.',dest='model_in',required=True)
    parser.add_argument('-tex','--texture-in', help='PNG texture to be processed.',dest='texture_in',required=True)
    parser.add_argument('-name','--item-name', help='The prefix that will be assigned to all relevant files.',dest='item_name',required=True)
    parser.add_argument('-pkg','--package-out', help='Package directory to be exported to',dest='pkg_out')
    parser.add_argument('-skmat','--skip-mat', help='Skip generating materials.',dest='skip_mat',action='store_true')
    parser.add_argument('-scomp','--skip-compile', help='Skip model compilation.',dest='skip_compile',action='store_true')
    parser.add_argument('-matdir','--mat-override', help='Override materials.',dest='override_mat')
    parser.add_argument('-mdldir','--model-override', help='Override model.',dest='override_model')
    args = parser.parse_args()


    #--------- SET DEFAULTS AND OVERRIDES ---------#

    loc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"..\\"))
    temp_dir = os.path.join(loc_dir,'temp\\')

    config = json.loads(open(os.path.join(loc_dir,"config.json"),"r").read())
    
    output = {
        'model_dir':f'props_map_editor\\{args.item_name}.mdl',
        'material_dir':f'props_map_editor\\{args.item_name}.vmt',
        'icon_dir':f'props_map_editor\\{args.item_name}.vtf'
    }

    activity = "checking overrides"
    
    if (args.override_model):
        output['model_dir'] = args.override_model
    if (args.override_mat):
        output['material_dir'] = args.override_mat

    #--------- RESIZE PNG IMAGES ---------#

    activity = "processing textures"
    if not args.skip_mat:
        img_icon = Image.open(args.texture_in)
        img_icon_small = img_icon.resize((64,64), Image.ANTIALIAS)
        img_icon_large = img_icon.resize((256,256), Image.ANTIALIAS)
        img_icon_small.save(os.path.join(temp_dir,'icon_small.png'))
        img_icon_large.save(os.path.join(temp_dir,'icon_large.png'))


    #--------- GENERATE QC FILE ---------#

    activity = "generating QC file"
        
    qc = {
        'export_path':output['model_dir'],
        'cd_mats':os.path.dirname(output['material_dir']),
        'smd_path':os.path.join(temp_dir,"Collection.smd")
    }
    gen_qc.saveQC(qc,os.path.join(temp_dir,"Collection.qc"))


    #--------- GENERATE VTF FILE ---------#

    activity = "generating VTF file"
    if not args.skip_mat:
        vprocess = subprocess.run([os.path.join(loc_dir,'exe\\VTFLib x64\\VTFCmd.exe'),
                                   '-file', os.path.join(temp_dir,'icon_large.png'),
                                   '-output',temp_dir
                                   ],stdout=subprocess.PIPE)


    #--------- GENERATE VMT FILE ---------#

    #if not args['skip_mat']:
        activity = "generating VMT file"
        gen_qc.saveVMT(
            output['icon_dir'],
            os.path.join(temp_dir,"icon_large.vmt")
    )


    #--------- RUN BLENDER ---------#

    activity = "running blender"
    bprocess = subprocess.run([os.path.join(loc_dir,config['blender_path']),'-b',os.path.join(loc_dir,'resources\\default.blend'),
                               '-x','0',
                               '--python-exit-code','1',
                               '--python',os.path.join(loc_dir,'resources\\blender_run.py'),
                               '--',
                               '-mi',args.model_in,
                               '-tx',args.texture_in,
                               '-mo',temp_dir,
                               '-ep',os.path.join(config['p2_folder'],'bin\\'),
                               '-mn',os.path.basename(output['material_dir'])
                               ],stdout=subprocess.PIPE)

    #--------- COMPILE MODEL ---------#

    if not args.skip_compile:
        activity = "compiling model"
        stprocess = subprocess.run([os.path.join(config['p2_folder'],'bin\\studiomdl.exe'),
                                    '-game',os.path.join(config['p2_folder'],'portal2\\'),
                                    os.path.join(temp_dir,'Collection.qc')
                                       ],stdout=subprocess.PIPE)


    #--------- COPY COMPILED MODEL ---------#

        shutil.copy(os.path.join(config['p2_folder'],'portal2\\models',output['model_dir']),os.path.join(temp_dir,os.path.basename(output['model_dir'])))

        
except Exception as e:
    print("\n\nAn error occurred while "+activity+". Error code:\n\n"+str(e)+"\n\n")