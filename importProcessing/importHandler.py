import ast


class Import():
    def __init__(self, module, name, alias, path):
        self.module = module
        self.name = name
        self.alias = alias
        self.path = path


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