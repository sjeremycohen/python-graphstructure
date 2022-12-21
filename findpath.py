import os
import sys
from collections import deque


# This program produces all the possible subdirectories that could contain modules given the current sys.path
def findpath(paths=sys.path):
    dirs = deque()

    # queue sys.path
    for path in paths:
        dirs.append(path)

    # create set to hold the visited dirs
    visited = set()
    packages = []

    while dirs:
        dirpath = dirs.popleft()
        if dirpath in visited:
            continue
        visited.add(dirpath)
        packages.append(dirpath)

        for root, subdirs, files in os.walk(dirpath):
            for subdir in subdirs:
                subdir_path = os.path.join(dirpath, subdir)
                init_path = os.path.join(subdir_path, "__init__.py")
                if os.path.exists(init_path):
                    dirs.append(subdir_path)

    return packages
    
if __name__=="__main__":
    print(findpath())