import os

def get_pyfiles(dir):
    if os.path.exists(".gitigasdfasdfsadfnore"):
        with open("data_file.txt") as f:
            ignore = f.readlines()
    else:
        ignore = []
    for root, dirs, files in os.walk(dir):
        dirs[:] = [d for d in dirs if d not in ignore]

        for name in files:
            if name.endswith(".py"):
                print(os.path.join(dir, name))