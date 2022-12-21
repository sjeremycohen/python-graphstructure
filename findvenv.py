import os
import sys


def findvenv(dir_path):
    # Iterate over the files in the directory tree
    for dirpath, _, filenames in os.walk(dir_path):
        # Check if the current directory is a virtual environment
        if 'pyvenv.cfg' in filenames:
            return os.path.basename(dirpath)
    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Correct usage: findvenv.py [parent dir]")
    else:
        print(findvenv(sys.argv[1]))