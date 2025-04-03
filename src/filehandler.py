import os
import shutil


def duplicate_directory(origin, destiny):
    elements_in_dir = os.listdir(origin)

    if len(elements_in_dir) == 0:
        print(f"No more files in {origin} to copy")
        return

    for element in elements_in_dir:
        new_path_origin = os.path.join(origin, element)
        new_path_destiny = os.path.join(destiny, element)
        print(f"Making copy of {new_path_origin}")
        if os.path.isdir(new_path_origin):
            os.mkdir(new_path_destiny)
            duplicate_directory(new_path_origin, new_path_destiny)
        else:
            shutil.copy(new_path_origin, new_path_destiny)


def static_files_handler(dir_path_public):
    path = os.getcwd()
    path_origin = os.path.join(path, "static")
    path_destiny = os.path.join(path, "docs")

    if os.path.exists(path_destiny):
        shutil.rmtree(path_destiny)

    os.mkdir(path_destiny)

    if not os.path.exists(path_origin):
        print(f"There is no files in {path_origin} to copy")
        return

    duplicate_directory(path_origin, path_destiny)
