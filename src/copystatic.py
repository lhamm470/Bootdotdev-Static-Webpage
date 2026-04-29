import os
import shutil

def move_directory(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)

    def copy_files_recursive(source_path, destination_path):
        for item in os.listdir(source_path):
            path = os.path.join(source_path, item)
            print(f" * {path} -> {os.path.join(destination_path, item)}")
            if os.path.isfile(path):
                shutil.copy(path, destination_path)
            elif os.path.isdir(path):
                os.mkdir(os.path.join(destination_path, item))
                copy_files_recursive(path, os.path.join(destination_path, item))
    copy_files_recursive(source_path, destination_path)