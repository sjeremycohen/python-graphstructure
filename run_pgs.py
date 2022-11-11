import sys
import networkx as nx
from importProcessing.importHandler import get_imports


def main():
    print("hi")
    args = sys.argv
    path = args[1] # given directory
    impts = get_imports(path)
    G = nx.Graph()
    G.add_nodes_from(impts)
    for impt in impts:
        print(impt)
    
if __name__ == '__main__':
    main()
    
    