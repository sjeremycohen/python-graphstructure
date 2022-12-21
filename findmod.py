import sys
import os
import fnmatch
from ex_paths import find_paths

def findmod(module_name, gitignore=False):
    if gitignore:
        with open('.gitignore', 'r') as f:
            patterns = f.read().splitlines()
            patterns = [s for s in patterns if s and not s.startswith("#")]
            print(patterns)

    for path in find_paths():
        module_pathname = module_name.replace('.','/')
        module_path = os.path.join(path, module_pathname)
        if os.path.exists(module_path + ".py"):
            # Check if the module is listed in the .gitignore file
            if gitignore:
                if any(fnmatch.fnmatch(module_path, pattern) for pattern in patterns):
                    return f"{module_name} is listed in {gitignore} and will be ignored by Git."
            return module_path + ".py"
    
    # We want to look for a .py file before we look for a package directory, as within a project the .py is more likely what we want.
    for path in find_paths():
        module_pathname = module_name.replace('.','/')
        module_path = os.path.join(path, module_pathname)
        if os.path.exists(module_path):
            # Check if the module is listed in the .gitignore file
            if gitignore:
                if any(fnmatch.fnmatch(module_path, pattern) for pattern in patterns):
                    return f"{module_name} is listed in {gitignore} and will be ignored by Git."
            return module_path

    return f"Module {module_name} not found in sys.path."

if __name__=="__main__":
    argc = len(sys.argv)
    if argc == 2:
        print(findmod(sys.argv[1]))
    if argc == 3:
        print(findmod(sys.argv[1], True))