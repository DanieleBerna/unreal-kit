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

open_file_dialog = filedialog.askopenfilenames( parent=root, initialdir='/', initialfile='tmp', filetypes=_IMPORTABLE_FILETYPES)
if open_file_dialog:
    print open_file_dialog
else:
    print("No file selected")
root.destroy()

