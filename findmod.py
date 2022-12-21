import sys
import os
from findpath import findpath


def findmod(module_name, paths):
    module_name = module_name.replace(".py", "")
    for path in paths:
        module_pathnames = [module_name.replace('.','/') + ".py", module_name.replace('.','/')]
        for module_pathname in module_pathnames:
            module_path = os.path.join(path, module_pathname)
            if os.path.exists(module_path):
                return module_path

    return f"Module {module_name} not found in python path."

if __name__=="__main__":
    if len(sys.argv) != 2:
        "Correct usage: python findmod.py [name of module]"
    print(findmod(sys.argv[1], findpath()))