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
