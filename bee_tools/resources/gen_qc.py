#Generate puzzlemaker QC file

def saveQC(props,di):
    q = open(di,"w")
    q.write(f'''$modelname "{props['export_path']}"
$body mybody "{props['smd_path']}"
$surfaceprop "metalpanel"
$contents "solid"
$mostlyopaque
$cdmaterials "{props['cd_mats']}"
$cdmaterials "BEE2\\{props['cd_mats']}"
$cbox 0 0 0 0 0 0
$sequence "idle" "{props['smd_path']}"
''')
    q.close()

def saveVMT(tex_path,di):
    q = open(di,"w")
    q.write('''UnLitGeneric
{
    $baseTexture "'''+tex_path+'''"
    $translucent
}''')
    q.close()
