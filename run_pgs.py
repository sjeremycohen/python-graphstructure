import sys
import networkx as nx
from importProcessing.importHandler import get_imports
from pathlib import Path
from fileStructure import get_pyfiles
from modulefinder import ModuleFinder


def main():
    args = sys.argv
    #filepath = args[1] # given directory
    #files = get_pyfiles(filepath)

    finder = ModuleFinder()
    finder.run_script('importProcessing/importHandler.py')
    print('Loaded modules:')
    for name, mod in finder.modules.items():
        print('%s: ' % name, end='')
        print(','.join(list(mod.globalnames.keys())[:3]))

    #print('-'*50)
    #print('Modules not imported:')
    #print('\n'.join(finder.badmodules.keys()))

    #impts = get_imports(filepath)
    #G = nx.Graph()
    #G.add_nodes_from(impts)
    #for file in files:
    #    print(file)
    #for impt in impts:
    #    print(impt.name)

    
if __name__ == '__main__':
    main()
    
    