import os
import shutil

def path_trimmer(file_paths, file_contents, folders, venv_path=""):

    file_paths = [os.path.normpath(path) for path in file_paths]
    folders = [os.path.normpath(folder) for folder in folders]
    # normalizing all of the paths to avoid malformed paths after trimming

    folder_prefix = os.path.commonpath(folders) if len(folders) > 1 else ""
    file_prefix = os.path.commonpath(file_paths) if len(file_paths) > 1 else ""
    # isolates the common base from paths such as ../../Project
    # removing instance of 1 element list because commonpath returns whole string if there's one elem

    print(file_prefix)

    trimmed_folders, trimmed_files = [], []
    # create the trimmed path lists

    folder_prefix_len = len(folder_prefix)
    file_prefix_len = len(file_prefix)
    # get length of prefix, should make slicing faster

    if len(file_paths) == 1:
        trimmed_files.append(os.path.basename(file_paths[0]))
    else:
        for file in file_paths:
            trimmed_files.append(file[file_prefix_len+1:])
        # populate trimmed path lists
    if len(folders) == 1:
        trimmed_folders.append(os.path.basename(folders[0]))
    else:
        for folder in folders:
            trimmed_folders.append(folder[folder_prefix_len+1:])
    
    return list(zip(trimmed_files, file_contents)), trimmed_folders, venv_path[folder_prefix_len+1:]

def create_folders(dest_path, folder_paths):
    os.makedirs(dest_path)   # recreate the destination path
    
    for folder in folder_paths:
        print("Creating: ", folder)
        if not os.path.isdir(os.path.join(dest_path, folder)):
            os.makedirs(os.path.join(dest_path, folder))

def create_files(dest_path, file_tree_info):
    for file in file_tree_info:
        print("Creating: ", file[0])
        file_path = file[0]

        try:
            with open(os.path.join(dest_path, file_path), "w") as new_file:
                new_file.write(file[1])
        except PermissionError as e:
            print(f"[ERROR] Permission denied for: {file_path}. Skipping...")
            continue
        except FileNotFoundError as e:
            print(f"[ERROR] File Not Found: {file_path}. Skipping...")
            
    if not os.path.isfile(os.path.join(dest_path, "__init__.py")):
        with open(os.path.join(dest_path, "__init__.py"), "w"):
            pass
        # make the code_files directory a module if it isn't already

def setup(dest_path):
    if os.path.isdir(dest_path):
        shutil.rmtree(dest_path) # remove the file tree recreation destination for repopulation

def read(file_path):
    contents = ""
    try:
        with open(file_path, "r") as file_contents:
            for line in file_contents.readlines():
                contents += line
        return contents
    except UnicodeDecodeError as e:
        return ""

def collector(path, file_paths = [], file_contents = [], folder_paths = [], venv_path = []): #lists are instantiated on function definition
    results = os.listdir(path)
    if is_venv(path, results):
        venv_path.append(path)
    for result in results:
        if "GUIPyDebugger" in result:  #don't duplicate the package that is running the script
            print("Skipping GUIPyDebugger package")
            continue    # not a problem if package script isn't inside of current debugging target
        relative_path = os.path.join(path, result)
        if os.path.isdir(relative_path):
            print("Spawning search job for: ", result)
            collector(relative_path)
            folder_paths.append(relative_path)
            # append folder paths to folder_paths
        else:
            print("Spawning read job for: ", result)
            file_content = read(os.path.join(path, result))
            file_paths.append(os.path.join(path, result))
            file_contents.append(file_content)
            # append file contents and file paths to respective lists

    return file_paths, file_contents, folder_paths, venv_path

def is_venv(path, results):
    if "Include" in results and "Lib" in results and "Scripts" in results:
        return path
    else:
        return ""

def main(src_path, dest_path):  
    if not os.path.isdir(src_path):
        print("[ERROR] Path Not Found: ", src_path)
        return False

    file_paths, file_contents, folder_paths, venv_path = collector(src_path)

    if len(venv_path) != 0:
        file_tree_info, folder_paths, venv_path = path_trimmer(
                        file_paths, file_contents, folder_paths, venv_path)
    else:
                file_tree_info, folder_paths, venv_path = path_trimmer(
                        file_paths, file_contents, folder_paths)

    create_folders(dest_path, folder_paths)

    create_files(dest_path, file_tree_info)

    print("\nYour debugging server can be found at >>> \033[34m http://127.0.0.1:8000\n \033[0m")

    return venv_path