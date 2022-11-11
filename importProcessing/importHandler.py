import ast
from collections import namedtuple

Import = namedtuple("Import",["module", "name", "alias"])

def get_imports(path):
    with open(path) as fh:
        root = ast.parse(fh.read(), path)
        
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):  
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)