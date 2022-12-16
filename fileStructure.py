import os
import sys


root_dir = sys.argv[1]

for root, dirs, files in os.walk(root_dir, topdown=True):
    print(os.path.basename(root))
    for file in files:
        if file.endswith(".py"):
            print(file)