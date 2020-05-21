import bpy
from os import path

def example_function(model_in, arg_img):
    # Clear existing objects.

    try:
        #my_model = bpy.ops.import_scene.obj(filepath=path.abspath(model_in), axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")
        my_model = bpy.ops.import_scene.obj(filepath=model_in, filter_glob="*.obj", use_image_search=False)
        mdl = bpy.data.objects[0] #3 == floor
        
        mat_new = bpy.data.materials.new("mat_default")
        mat_new.use_nodes = True
        
        bsdf = mat_new.node_tree.nodes["Principled BSDF"]
        mat_tex = mat_new.node_tree.nodes.new('ShaderNodeTexImage')
        mat_tex.image = bpy.data.images.load(filepath = arg_img)
        mat_new.node_tree.links.new(bsdf.inputs['Base Color'], mat_tex.outputs['Color'])
        
        mdl.data.materials[0] = (mat_new)
        
        bpy.context.scene.render.filepath = '//../../bee_tools/temp/icon_rendered.png'
        bpy.ops.render.render(write_still = True)
    except Exception as e:
        print("\n\n\nERROR: "+str(e)+"\n\n\n")
        exit()

def main():
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message

    # get the args passed to blender after "--", all of which are ignored by
    # blender so scripts may receive their own arguments
    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    # When --help or no args are given, print this help
    usage_text = (
        "Run blender in background mode with this script:"
        "  blender --background --python " + __file__ + " -- [options]"
    )

    parser = argparse.ArgumentParser(description=usage_text)

    # Example utility, add some text and renders or saves it (with options)
    # Possible types are: string, int, long, choice, float and complex.
    parser.add_argument(
        "-mi", "--model_in", dest="model_in", type=str, required=True,
        help="Model in",
    )

    parser.add_argument(
        "-tx", "--texture_in", dest="texture_in", metavar='FILE',
        help="Texture in",
    )

    args = parser.parse_args(argv)  # In this example we won't use the args

    if not argv:
        parser.print_help()
        return

    if not args.model_in:
        print("Error: --text=\"some string\" argument not given, aborting.")
        parser.print_help()
        return

    # Run the example function
    example_function(args.model_in, args.texture_in)


if __name__ == "__main__":
    main()
