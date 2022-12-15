import ast
import os
import sys

# Get the filename of the file to parse
filename = sys.argv[1]

# Open the file and parse its AST
with open(filename, 'r') as file:
    tree = ast.parse(file.read())

# Find all the import statements in the AST
imports = [node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]

# Print the names and locations of the imported files
for imp in imports:
    if isinstance(imp, ast.Import):
        for name in imp.names:
            print(f'{name.name} is located at {os.path.join(os.path.dirname(filename), name.name)}')
    elif isinstance(imp, ast.ImportFrom):
        print(f'{imp.module} is located at {os.path.join(os.path.dirname(filename), imp.module)}')