import importlib
from io import StringIO
import os
import sys

def find_entry_point(code_files_path, entry_point_string):

    entry_point_path, entry_point_name = None, None

    for dirpath, _, filenames in os.walk(code_files_path):
    # traverse replicated file tree
        for filename in filenames:
            if ".py" in filename and filename[-1] != "c":
                # ignore .pyc files
                with open(os.path.join(dirpath, filename), "r") as file:
                    first_line = file.readline()
                    if first_line == entry_point_string:
                        file_contents = ''.join(file.readlines())
                        entry_point_path = os.path.join(dirpath, filename)
                        entry_point_name = filename
            if entry_point_path != None:
                break
        if entry_point_path != None:
            break
    
    return entry_point_name, entry_point_path

def dynamic_import(entry_point_name, entry_point_path):
    spec = importlib.util.spec_from_file_location(entry_point_name, entry_point_path)

    module = importlib.util.module_from_spec(spec)

    sys.modules[entry_point_name] = module

    temp_stdout = StringIO()

    sys.stdout = temp_stdout
    # redirected so print statements from code do not run in main console
    # I might throw the output in a text file later

    original_dir = os.getcwd()
    entry_dir = entry_point_path.rstrip(os.path.basename(entry_point_path))
    # for changing directories to make file IO work during execution

    try:
        # remove the filename from the path, that is the context the script is meant to run in
        os.chdir(entry_dir)
        spec.loader.exec_module(module)
    except ImportError as e:
        os.chdir(original_dir)
        sys.stdout = sys.__stdout__
        print(f"Error while loading module {entry_point_name}: {e}")
        print("Modules with code other than python cannot be dynamically imported such as numpy")
        raise ImportError
    except FileNotFoundError as e:
        os.chdir(original_dir)
        sys.stdout = sys.__stdout__
        print(f"Error while loading module: {entry_point_name}: {e}")
        raise FileNotFoundError

    os.chdir(original_dir)
    sys.stdout = sys.__stdout__
    # restore stdout and directory

    return module

