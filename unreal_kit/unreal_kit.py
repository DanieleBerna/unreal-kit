import unreal as ue
import os
import re
import getpass

_RAW_FOLDER = "Raw"
_DEVELOPER_FOLDER = "Developers"
_IMPORT_FOLDER = "Import"
_IMPORTABLE_FILETYPES = {"FBX":"*.fbx .FBX", "TGA":"*.tga", "PNG":"*.png", "PSD":"*.psd", "JPEG":"*.jpg", "All files":"*"}


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

    _IMPORTABLE_FILETYPES = [("FBX", "*.fbx .FBX"), ("TGA", "*.tga"), ("PNG", "*.png"), ("PSD", "*.psd"), ("JPEG", "*.jpg"),("All files", "*")]
    root = tk.Tk()
    # Setting icon of master window
    window_icon = tk.PhotoImage(file='T:\\ugcore\\rez\\packages\\unrealengine\\unreal_icon.gif')
    root.tk.call('wm', 'iconphoto', root._w, window_icon)
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


def open_folder_dialog(start_folder="./"):
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
    # Setting icon of master window
    window_icon = tk.PhotoImage(file='T:\\ugcore\\rez\\packages\\unrealengine\\unreal_icon.gif')
    root.tk.call('wm', 'iconphoto', root._w, window_icon)
    root.withdraw()
    style = ttk.Style(root)
    style.theme_use("vista")

    open_file_dialog = filedialog.askdirectory(parent=root, initialdir=start_folder)
    if open_file_dialog:
        print open_file_dialog
    else:
        print("No directory selected")
    root.destroy()
    return open_file_dialog


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
        task.destination_path = get_content_from_working_path(filename)
    else:
        task.destination_path = "/Game"  # Cambiare in modo che importi nella cartella attualmente selezionata
    task.automated = True
    return task


def parse_filename_parts(full_filename):

    # Nome del file senza il path ed estensione
    file_name_and_extension = re.split('\.', (os.path.split(full_filename)[1]))
    file_name_and_extension[1] = file_name_and_extension[1].lower()

    # Prefisso
    prefix = file_name_and_extension[0].split('_')[0]
    # controllare se esiste il prefisso

    suffix = file_name_and_extension[0].split('_')[-1]
    # controllare se esiste il suffisso

    # Ritorna la tupla (nome,estensione,prefisso,suffisso)
    return file_name_and_extension[0], file_name_and_extension[1], prefix, suffix


def import_file_from_task(import_task):
    if import_task:
        try:
            ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])

            imported_asset = None
            # Post-import assets editing
            for objectPath in import_task.imported_object_paths:

                # Controlla di che tipo di asset si tratta e se texture cambia il compression setting in modo appropriato
                file_type = parse_filename_parts(import_task.filename)[1]
                print("filetype: ")
                print(file_type)
                if file_type in ['tga', 'png', 'psd', 'jpg']:
                    texture_type = parse_filename_parts(import_task.filename)[3]

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

                elif file_type == "fbx":
                    mesh = ue.EditorAssetLibrary.load_asset(objectPath)
                    print(mesh)
                    new_material = ue.EditorAssetLibrary.load_asset("/Game/City20/Core/Graphics/Materials/ProceduralPalette/MI_City20Palette_01_Static_Opaque")
                    print(new_material)
                    mesh.set_material(mesh.get_material_index("MI_City20Palette_01"), new_material)

                if not imported_asset:
                    imported_asset = objectPath

            ue.EditorAssetLibrary().load_asset(imported_asset)
            print(get_asset_base_name(imported_asset))
            ue.EditorAssetLibrary().sync_browser_to_objects([imported_asset, ])
            return True
        except:
            return False


def list_files_in_folder(folder, include_subfolders):
    if include_subfolders:
        files_to_import = []
        file_types = ("fbx", "tga", "png", "jpg", "psd", "wav")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if os.path.isfile(os.path.join(root, file)):
                    if os.path.splitext(file)[1][1:] in file_types:
                        files_to_import += ((root + '/' + file).replace('\\', '/'),)
            if not include_subfolders:
                break
        return files_to_import


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

    @ue.ufunction(params=[str], ret=str, static=True, meta=dict(Category="Untold Games Python"))
    def bp_open_folder_dialog(start_dir):
        return open_folder_dialog(start_dir)

    @ue.ufunction(params=[str, bool], ret=ue.AssetImportTask, static=True, meta=dict(Category="Untold Games Python"))
    def bp_create_import_task(filename, mirror_path):
        return create_import_task(filename, mirror_path)

    @ue.ufunction(params=[ue.AssetImportTask], ret=bool, static=True, meta=dict(Category="Untold Games Python"))
    def bp_import_file_from_task(import_task):
        return import_file_from_task(import_task)

    @ue.ufunction(params=[str, bool], ret=ue.Array(str), static=True, meta=dict(Category="Untold Games Python"))
    def bp_list_files_in_folder(folder, include_subfolders):
        return list_files_in_folder(folder, include_subfolders)
