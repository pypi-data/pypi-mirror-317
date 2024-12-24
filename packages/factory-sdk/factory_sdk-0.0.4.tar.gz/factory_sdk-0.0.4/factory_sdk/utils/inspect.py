import inspect
import ast
import hashlib
import black

def get_function_dependencies(tree: ast.Module, func_name: str):
    """
    Given an AST and a function name, returns a set of function names (including
    the original) that need to be included. It finds all calls in the function’s 
    body and includes any functions defined in the same module.
    """
    func_map = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}

    to_visit = [func_name]
    included = set()

    while to_visit:
        current = to_visit.pop()
        if current in included:
            continue
        if current not in func_map:
            # Not defined in this module
            continue

        included.add(current)
        func_node = func_map[current]

        # Find all calls inside this function
        for call_node in ast.walk(func_node):
            if isinstance(call_node, ast.Call):
                # Check if the function is a simple Name call
                if isinstance(call_node.func, ast.Name):
                    called_func = call_node.func.id
                    # If this called_func is defined in the same module, we add it
                    if called_func in func_map and called_func not in included:
                        to_visit.append(called_func)
                # Additional logic could handle attributes, etc., but omitted for simplicity.

    return included

def remove_unused_imports(tree: ast.Module):
    """
    Remove unused import statements from the AST.
    - Collect all imported names.
    - Find which imported names are used.
    - Remove import statements for unused names.
    """
    imported_names = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            # e.g. `import math` -> {'math'}
            names = {alias.asname if alias.asname else alias.name.split('.')[0] for alias in node.names}
            imported_names[node] = names
        elif isinstance(node, ast.ImportFrom):
            # if from ... import *
            if any(alias.name == '*' for alias in node.names):
                imported_names[node] = None
            else:
                names = {alias.asname if alias.asname else alias.name for alias in node.names}
                imported_names[node] = names

    if not imported_names:
        return

    # Find all Names used in the code
    used_names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            used_names.add(n.id)

    new_body = []
    for node in tree.body:
        if node not in imported_names:
            new_body.append(node)
        else:
            names = imported_names[node]
            if names is None:
                # from ... import * -> keep it
                new_body.append(node)
            else:
                # Keep only if at least one name is used
                if any(name in used_names for name in names):
                    new_body.append(node)

    tree.body = new_body

def get_cleaned_module_source(obj):
    """
    Given a function object, return minimal source code containing:
    - The function itself
    - All local functions it depends on (recursively)
    - Module docstring (if present)
    - Necessary imports only (unused imports removed)
    - No global constants or assignments
    """
    file_path = inspect.getfile(obj)
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    tree = ast.parse(source_code)

    # Identify the target function name
    func_name = obj.__name__

    # Determine which functions need to be included
    needed_functions = get_function_dependencies(tree, func_name)

    # Filter the AST:
    # Keep:
    # - Module docstring (once)
    # - Imports
    # - Functions in needed_functions
    filtered_body = []
    docstring_included = False
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            filtered_body.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in needed_functions:
            filtered_body.append(node)
        elif (isinstance(node, ast.Expr) 
              and isinstance(node.value, ast.Constant)
              and isinstance(node.value.value, str) 
              and not docstring_included):
            # Module docstring
            filtered_body.append(node)
            docstring_included = True
        else:
            # Skip ClassDef, Assign, AnnAssign, etc.
            pass

    tree.body = filtered_body

    # Remove unused imports
    remove_unused_imports(tree)

    # Unparse the cleaned AST
    cleaned_code = ast.unparse(tree)

    # Format the code with Black (if available) to improve code formatting
   
    cleaned_code = black.format_str(cleaned_code, mode=black.FileMode())

    return file_path, func_name, cleaned_code

def hash_code_by_ast(source_code: str) -> str:
    # Hash the AST representation of the code
    tree = ast.parse(source_code)
    ast_repr = ast.dump(tree, include_attributes=False)
    hash_obj = hashlib.md5()
    hash_obj.update(ast_repr.encode('utf-8'))
    return hash_obj.hexdigest()
