import sys
import networkx as nx
from importProcessing.importHandler import get_imports
from pathlib import Path
from fileStructure import get_pyfiles



def main():
    args = sys.argv
    filepath = args[1] # given directory
    files = get_pyfiles(filepath)
    #impts = get_imports(filepath)
    #G = nx.Graph()
    #G.add_nodes_from(impts)
    #for file in files:
    #    print(file)
    #for impt in impts:
    #    print(impt.name)

    
if __name__ == '__main__':
    main()
    
    