import os
_RAW_FOLDER = "Raw"

filename="D:/Works/City20/Raw/Import/Items/Weapons/Bow"
folders_list = os.path.dirname(filename).split(_RAW_FOLDER)[1].replace(os.sep, '/').split('/')[1:]
print(folders_list)