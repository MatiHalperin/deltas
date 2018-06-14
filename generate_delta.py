import filecmp
import os
from shutil import copy2, copytree
import sys

old_folder = sys.argv[1]
new_folder = sys.argv[2]
target_folder = sys.argv[3]

def CopyFile(source_file, destination_file):
    if not os.path.exists(os.path.dirname(destination_file)):
        os.makedirs(os.path.dirname(destination_file))

    copy2(source_file, destination_file)

def FilesToCopy(current_folder=""):
    for archive in os.listdir(new_folder + "/" + current_folder):
        filename = current_folder + "/" + archive

        new_file = new_folder + filename
        old_file = old_folder + filename
        target_file = target_folder + "/system" + filename

        if os.path.isdir(new_file) and not os.path.isdir(old_file):
            copytree(new_file, target_file)
        elif os.path.isfile(new_file) and not os.path.isfile(old_file):
            CopyFile(new_file, target_file)
        else:
            if os.path.isdir(new_file):
                FilesToCopy(filename)
            elif os.path.isfile(new_file) and not filecmp.cmp(old_file, new_file):
                CopyFile(new_file, target_file)

def FilesToDelete(current_folder=""):
    for archive in os.listdir(old_folder + "/" + current_folder):
        filename = current_folder + "/" + archive

        new_file = new_folder + "/" + filename
        old_file = old_folder + "/" + filename

        if (os.path.isdir(old_file) and not os.path.isdir(new_file)) or (os.path.isfile(old_file) and not os.path.isfile(new_file)):
            with open(target_folder + "/delete/delete_file", "a") as delete_file:
                delete_file.write("/system" + filename + "\n")
        elif os.path.isdir(old_file):
            FilesToDelete(filename)

FilesToCopy()
FilesToDelete()