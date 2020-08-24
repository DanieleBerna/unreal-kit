import unreal as ue
import os
import getpass

_RAW_FOLDER = "Raw"
_DEVELOPER_FOLDER = "Developers"
_IMPORT_FOLDER = "Import"


def get_ue_project_root():
    return ue.SystemLibrary.get_project_directory()


def get_content_folder():
    return ue.SystemLibrary.get_project_content_directory()


def get_asset_base_name(asset_path):
    return (str(ue.AssetData(object_path=asset_path).get_full_name())).split('.')[-1]


def get_content_from_working_path(filename):
    project_name = ue.SystemLibrary.get_game_name()
    final_path = ""

    folders_list = os.path.dirname(filename).split(_RAW_FOLDER)[1].replace(os.sep, '/').split('/')[1:]
    print("folders_list")
    print(folders_list)
    first_folder = folders_list[0]
    print("first_folder")
    print(first_folder)
    print("path_to_mirror")
    path_to_mirror = "/"+"/".join(folders_list[1:])
    print(path_to_mirror)

    # path_part_to_mirror = filename.split("ImportFiles")[1].replace(os.sep, '/')

    if first_folder == _DEVELOPER_FOLDER:
        final_path = ("/Game/Developers/"+(getpass.getuser().replace(".", ""))+path_to_mirror).replace(os.sep, '/')
    elif first_folder == _IMPORT_FOLDER:
        final_path = ("/Game/"+project_name+path_to_mirror).replace(os.sep, '/')
    else:
        final_path = ""

    print(final_path)
    return final_path


def open_file_dialog(start_folder="./"):
    try:
        import tkinter as tk
        import tkinter.ttk as ttk
        from tkinter import filedialog
    except ImportError:
        import Tkinter as tk
        import ttk
        import tkFileDialog as filedialog

    _IMPORTABLE_FILETYPES = [("PNG", "*.png"),("JPEG", "*.jpg"),("All files", "*")]
    root = tk.Tk()
    root.withdraw()
    style = ttk.Style(root)
    style.theme_use("vista")

    open_file_dialog = filedialog.askopenfilenames( parent=root, initialdir=start_folder, initialfile='tmp', filetypes=_IMPORTABLE_FILETYPES)
    if open_file_dialog:
        print open_file_dialog
    else:
        print("No file selected")
    root.destroy()
    return open_file_dialog

@ue.uclass()
class UntoldBPFunctionLibrary(ue.BlueprintFunctionLibrary):

    @ue.ufunction(static=True, ret=str, meta=dict(Category="Untold Games Python"))
    def bp_get_ue_project_root():
        return get_ue_project_root()

    @ue.ufunction(static=True, ret=str, meta=dict(Category="Untold Games Python"))
    def bp_get_content_folder():
        return get_content_folder()

    @ue.ufunction(params=[str], ret=str, static=True, meta=dict(Category="Untold Games Python"))
    def bp_get_asset_base_name(asset_path):
        return get_asset_base_name(asset_path)

    @ue.ufunction(params=[str], ret=str, static=True, meta=dict(Category="Untold Games Python"))
    def bp_get_content_from_working_path(filename):
        return get_content_from_working_path(filename)

    @ue.ufunction(params=[str], ret=ue.Array(str), static=True, meta=dict(Category="Untold Games Python"))
    def bp_open_file_dialog(start_dir):
        return open_file_dialog(start_dir)








def get_content_from_working_path_OLD(filename):
    project_name = ue.SystemLibrary.get_game_name()
    # asset_origin = ""
    final_path = ""

    split = filename.split("ImportFiles")
    finale = ("/Game/"+project_name+split[1]).replace(os.sep, '/')
    print("Percorso finale:" +finale+"\neccolo")

    if (project_name+"/DeveloperFiles") in filename:
        path_part_to_mirror = filename[len(os.path.join(get_ue_project_root(), "DeveloperFiles", 'import_files')):]
        final_path = os.path.join("/Game", "Developers", getpass.getuser().replace(".", ""), path_part_to_mirror).replace(os.sep, '/')
    else:
        path_part_to_mirror = filename[len(os.path.join(get_ue_project_root(), "AssetsFiles", 'import_files')):]
        final_path = os.path.join("/Game", project_name, path_part_to_mirror).replace(os.sep, '/')

    # print (asset_origin)
    # path_part_to_mirror = filename[len(os.path.join(get_ue_project_root(), asset_origin, 'import_files')):]
    return final_path


def spawn_from_content_object(object_fullpath, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    loaded_object = ue.EditorAssetLibrary.load_asset(object_fullpath)
    if loaded_object:
        """location = ue.Vector()
        location.x = 0
        location.y = 0
        location.z = 0
        rotation = ue.Rotator()"""
        spawned_actor = ue.EditorLevelLibrary.spawn_actor_from_object(loaded_object, location, rotation)
        return spawned_actor


def get_level_assets_by_name(asset_name, asset_class=None):

    actor_list = ue.EditorFilterLibrary.by_actor_label(ue.EditorLevelLibrary.get_all_level_actors(), asset_name,
                                                       ue.EditorScriptingStringMatchType.MATCHES_WILDCARD)
    if asset_class is not None:
        actor_list = ue.EditorFilterLibrary.by_class(actor_list, asset_class)

    return actor_list


def mirrored_asset_path(asset_fullpath):
    name_parts = asset_fullpath.split("/")

    asset_name = name_parts[-1]
    asset_content_path = "/"+(os.path.join(*name_parts[0:-1])).replace("\\", "/")+"/"
    mirrored_path = asset_content_path.replace("/Game/"+ue.SystemLibrary.get_game_name()+"/", "")
    return asset_name, asset_content_path, mirrored_path


def create_new_asset(asset_name, package_path="/Game", asset_class=ue.DataTable):
    factory = ue.SoundFactory()
    asset_tools = ue.AssetToolsHelpers.get_asset_tools()
    # new_asset = asset_tools.create_asset(asset_name, package_path, None, factory)

    new_asset = asset_tools.create_asset("test2", "/Game/junk/", None, ue.DataTableFactory())

    ue.EditorAssetLibrary.save_loaded_asset(new_asset)
    return new_asset


def duplicate_asset(source_asset_fullpath, destination_path=None, new_name=None):
    source_name, source_path, _ = mirrored_asset_path(source_asset_fullpath)
    if destination_path is None:
        destination_path = source_path

    if new_name is None and destination_path == source_path:
        new_name = source_name + "_copy"

    elif new_name is None and destination_path != source_path:
        new_name = source_name

    return ue.EditorAssetLibrary.duplicate_asset(source_asset_fullpath, destination_path+"/"+new_name)


def get_static_mesh_component_rotations(sm_comp, relative=True):
    comp_name = sm_comp.get_name()
    comp_rot = None
    if relative:
        comp_rot = sm_comp.get_editor_property("relative_rotation")
        # comp_rot = sm_comp.get_relative_rotation()
    else:
        comp_rot = sm_comp.get_world_rotation()
    return {"Name": comp_name, "yaw": comp_rot.yaw, "pitch": comp_rot.pitch, "roll": comp_rot.roll}


def get_all_static_mesh_components_rotations(actor):
    sm_comps = actor.get_components_by_class(ue.StaticMeshComponent)
    data = []
    for sm_comp in sm_comps:
        data.append(get_static_mesh_component_rotations(sm_comp))
    return data


"""def write_rotations_data_table(actor, data_table):
    if data_table is not None:
        table_namemirrored_asset_path(data_table)
        project_folder = ue.SystemLibrary.get_project_directory()
        json_file = os.path.join(project_folder, mirrored_asset_path(data_table)"rotations.json")
        with open(json_file, 'w') as outfile:
            json.dump(get_all_static_mesh_components_rotations(actor), outfile)
        ue.DataTableFunctionLibrary.fill_data_table_from_json_file(data_table, json_file)
        return"""


def create_blueprint(bp_name, package_path="/Game/Blueprints", parent_class=ue.Actor):

    factory = ue.BlueprintFactory()
    factory.set_editor_property("ParentClass", parent_class)

    asset_tools = ue.AssetToolsHelpers.get_asset_tools()
    new_blueprint = asset_tools.create_asset(bp_name, package_path, None, factory)

    ue.EditorAssetLibrary.save_loaded_asset(new_blueprint)

    return new_blueprint


def export_mesh2(asset, export_folder):

    ue.AssetToolsHelpers.get_asset_tools().export_assets([asset], export_folder)

    filename = (asset.split("/")[-1])+".fbx"
    filepath = asset.replace(asset.split("/")[-1], "")
    source = export_folder+filepath+filename
    destination = os.path.join(export_folder, filename)
    os.rename(source, destination)
    for dir_to_delete, _, _ in os.walk(os.path.join(export_folder, "Game"), topdown=False):
        os.rmdir(dir_to_delete)


def import_animation_fbx(animation_fbx_filename, skeleton):
    task = ue.AssetImportTask()
    task.filename = animation_fbx_filename

    task.options = ue.FbxImportUI()
    task.options.automated_import_should_detect_type = True
    task.options.mesh_type_to_import = ue.FBXImportType.FBXIT_SKELETAL_MESH
    # task.options.import_as_skeletal = False
    task.options.skeleton = ue.load_asset(skeleton)
    task.options.import_mesh = False
    task.options.import_animations = True
    task.options.create_physics_asset = False
    task.options.import_materials = False
    task.options.import_textures = False
    task.destination_path = get_content_from_working_path(os.path.dirname(animation_fbx_filename))
    task.automated = True

    ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    # remove not needed mesh asset and rename animation clip
    # THIS IS A TEMP FIX UNTIL import_meshes=False WON'T WORK
    base_name = os.path.basename(animation_fbx_filename).replace(".fbx", "")
    ue.EditorAssetLibrary.delete_asset(task.destination_path+"/"+base_name)
    ue.EditorAssetLibrary.rename_asset(task.destination_path+"/"+base_name+"_Anim", task.destination_path+"/"+base_name)


def export_fbx(asset_path, destination_folder=None):

    task = ue.AssetExportTask()
    task.object = ue.load_object(None, asset_path)
    print("Exporting object: {0}".format(task.object))
    if task.object is None:
        return

    asset_name, content_path, mirrored_path = mirrored_asset_path(asset_path)

    if not destination_folder:
        destination_folder = os.path.join(get_ue_project_root(), "AssetsFiles", "ImportFiles", mirrored_path)

    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)

    filename = os.path.join(destination_folder, asset_name + ".fbx")

    task.automated = True
    task.filename = filename
    task.selected = False
    task.replace_identical = True
    task.prompt = False
    task.use_file_archive = False
    task.write_empty_files = False

    fbx_export_options = ue.FbxExportOption()
    fbx_export_options.collision = True
    fbx_export_options.fbx_export_compatibility = ue.FbxExportCompatibility.FBX_2013
    fbx_export_options.force_front_x_axis = False
    fbx_export_options.level_of_detail = True
    fbx_export_options.map_skeletal_motion_to_root = False
    fbx_export_options.vertex_color = True
    task.options = fbx_export_options

    export_result = ue.Exporter.run_asset_export_tasks([task])
    print("Export result: {0}".format(export_result))

    return filename

def create_import_task(filename, mirror_path=True):
    task = ue.AssetImportTask()
    task.filename = filename

    file_type = os.path.splitext(filename)[1][1:]

    """In base all'estensione cambia cosa fa l'importer:
    1- FBX: crea un FbxImportUI come options e imposta i vari parametri. Poi stabilisce da solo se importarla come Static o Skeletal
    2- TGA, PNG, PSD, JPG: importa come texture e in base al suffisso decide quale compressione applicare"""

    if file_type == 'fbx':
        print('MESH')
        task.options = ue.FbxImportUI()
        task.options.automated_import_should_detect_type = True
        task.options.create_physics_asset = False
        task.options.import_materials = False
        task.options.import_textures = True
        task.options.static_mesh_import_data.combine_meshes = True

    elif file_type in ['tga', 'png', 'psd', 'jpg']:
        print('TEXTURE')

    if mirror_path:
        print("path "+filename)
        task.destination_path = get_content_from_working_path(os.path.dirname(filename))
    else:
        task.destination_path = "/Game"  # Cambiare in modo che importi nella cartella attualmente selezionata
    task.automated = True
    return task


def import_files(selected_files):
    tasks_list = []
    for f in selected_files:
        tasks_list.append(create_import_task(f))

    ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks_list)

    first_imported_object = None

    # Post-import assets editing
    for t in tasks_list:
        for objectPath in t.imported_object_paths:

            # Controlla di che tipo di asset si tratta e se texture cambia il compression setting in modo appropriato
            file_type = parse_filename_parts(t.filename)[1]
            if file_type in ['tga', 'png', 'psd', 'jpg']:
                texture_type = parse_filename_parts(t.filename)[3]

                if texture_type == 'M':  # MASKS
                    mask_texture=ue.EditorAssetLibrary.load_asset(objectPath)
                    mask_texture.compression_settings = ue.TextureCompressionSettings.TC_MASKS
                    mask_texture.srgb = False

                elif texture_type == 'N':  # NORMAL MAP
                    normal_texture = ue.EditorAssetLibrary.load_asset(objectPath)
                    normal_texture.compression_settings = ue.TextureCompressionSettings.TC_NORMALMAP

                elif texture_type == 'UI':  # USER INTERFACE
                    ui_texture = ue.EditorAssetLibrary.load_asset(objectPath)
                    ui_texture.compression_settings = ue.TextureCompressionSettings.TC_EDITOR_ICON

                elif texture_type in ('A', 'O', 'AO'):  # SINGLE GRAYSCALE MASK
                    grayscale_texture = ue.EditorAssetLibrary.load_asset(objectPath)
                    grayscale_texture.compression_settings = ue.TextureCompressionSettings.TC_GRAYSCALE

                elif texture_type in ('V', 'FM'):  # VECTOR DISPLACEMENT
                    vector_texture = ue.EditorAssetLibrary.load_asset(objectPath)
                    vector_texture.compression_settings = ue.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP

                elif texture_type == 'H':  # HDR
                    hdr_texture = ue.EditorAssetLibrary.load_asset(objectPath)
                    hdr_texture.compression_settings = ue.TextureCompressionSettings.TC_HDR

            if not first_imported_object:
                first_imported_object = objectPath

    ue.EditorAssetLibrary().load_asset(first_imported_object)
    print(get_asset_base_name(first_imported_object))

    ue.EditorAssetLibrary().sync_browser_to_objects([first_imported_object, ])


library = UntoldBPFunctionLibrary()
filename = "D:\\Works\\City20\\GameProject\\Raw\\Developers\\Items\\Junks\\object.fbx"
print(library.bp_get_content_from_working_path(filename))
