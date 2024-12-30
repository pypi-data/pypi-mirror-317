import ast
import os
import pkgutil
import re

def get_submodules(code):
    '''
    Used to grab submodules from code_files package (it's a package cause __init__.py is inserted by default)
    '''
    submodules = []
    chars_to_remove = len(r"static\code_files") + 1
    # can't think of a fancier way to specify this value...
    for module_finder, modname, ispackage in pkgutil.walk_packages(path=code.__path__, prefix=code.__name__ + '.'):
        submodules.append((modname[chars_to_remove:], module_finder.path, ispackage)) #removing the static directory from the beginning
    
    return submodules

def skip_comments_and_docstrings(src_code, line_no):
    line = src_code[line_no].strip()

    if not line or line.startswith("#"):
        line_no += 1
    # skips blank lines and comments

    if line.startswith("'''") or line.startswith('"""'):
        docstring_term_line_no = False
        if line.endswith("'''") or line.endswith('"""'):
            line_no += 1
            docstring_term_line_no = True
        while not docstring_term_line_no:
            line_no += 1
            line = src_code[line_no].strip()
            if "'''" in line or '"""' in line:
                line_no += 1
                break

    return line_no

def get_blocks(name, path):
    with open(os.path.join(path, name + ".py"), "r") as python_file:
        src_code = python_file.read()
    
    tree = ast.parse(src_code)
    blocks = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            block = {
                "type": "function",
                "name": node.name,
                "line_no": node.lineno,
                "docstring": ast.get_docstring(node),
                "args": [arg.arg for arg in node.args.args],
                "contents": ast.unparse(node) if hasattr(ast, "unparse") else "",
            }
            blocks.append(block)
        elif isinstance(node, ast.ClassDef):
            class_methods = []
            for class_node in node.body:
                if isinstance(class_node, ast.FunctionDef):
                    method = {
                        "name": class_node.name,
                        "line_no": class_node.lineno,
                        "docstring": ast.get_docstring(class_node),
                        "args": [arg.arg for arg in class_node.args.args],
                        "contents": ast.unparse(class_node) if hasattr(ast, "unparse") else "",
                    }
                    class_methods.append(method)
            block = {
                "type": "class",
                "name": node.name,
                "line_no": node.lineno,
                "docstring": ast.get_docstring(node),
                "methods": class_methods,
                "contents": ast.unparse(node) if hasattr(ast, "unparse") else "",
            }
            blocks.append(block)

    return blocks

def get_docstring(code):
    src_code = "\n".join(code)
    docstring_match = re.findall(r'"""(.*?)"""', src_code, re.DOTALL)

    if len(docstring_match) == 0:
        docstring_match = re.findall(r"'''(.*?)'''", src_code, re.DOTALL)
    # this catches ''' and """ docstrings
    

    if len(docstring_match) == 0:
        docstring_match.append("")
        # if no match is found just add an empty string

    docstring_match = docstring_match[0]

    return docstring_match

def get_local_var_names(block):
    tree = ast.parse(block)

    var_names = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_names.append(target.id)

    return var_names

def get_class_attrs(block):
    tree = ast.parse(block)

    class_attrs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    class_attrs.append(target.id)
    return class_attrs

def get_inst_attrs(block):
    tree = ast.parse(block)

    inst_attrs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
                    inst_attrs.append(target.attr)

    return inst_attrs

def get_methods(block):
    tree = ast.parse(block)

    methods = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)

    return methods

def master_dict_constructor(code):
    info = {"modules": []}
    submodules = get_submodules(code)

    for name, path, ispkg in submodules:
        if ispkg:
            continue
        name_slice = name[name.rfind(".") + 1:] if name.rfind(".") != -1 else name
        blocks = get_blocks(name_slice, path)

        functions = [block for block in blocks if block["type"] == "function"]
        classes = [block for block in blocks if block["type"] == "class"]

        module = {
            "name": name,
            "path": path,
            "functions": [
                {
                    "line_no": function["line_no"],
                    "signature": f"{function['name']}({', '.join(function['args'])})",
                    "docstring": function["docstring"],
                    "locals": get_local_var_names(function["contents"]),
                    "contents": function["contents"],
                }
                for function in functions
            ],
            "classes": [
                {
                    "line_no": cls["line_no"],
                    "signature": cls["name"],
                    "docstring": cls["docstring"],
                    "instance_attrs": get_inst_attrs(cls["contents"]),
                    "class_attrs": get_class_attrs(cls["contents"]),
                    "methods": cls["methods"],
                    "contents": cls["contents"],
                }
                for cls in classes
            ],
        }

        info["modules"].append(module)

    return info