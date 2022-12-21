import os
import sys
from graphimport import graphimport
from neo4j import GraphDatabase
from dotenv import load_dotenv


def findpyfiles(root_dir):
    # Create a list to hold the file paths
    py_files = []

    # Iterate over the files in the directory tree
    for dirpath, _, filenames in os.walk(root_dir):
        # Add the file paths of any .py files to the list
        py_files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.py')])

    return py_files


def graphpyproj(input):
    load_dotenv()
    #paths = findpath(sys.path)

    # Create a Neo4j driver to connect to the database
    n4js = os.environ.get('NEO4J_SERVER')
    n4jdb = os.environ.get('NEO4J_DB')
    n4jpw = os.environ.get('NEO4J_PW')

    driver = GraphDatabase.driver(n4js, auth=(n4jdb, n4jpw))

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    # If it's a file, just do the graphimport
    if ".py" in input:
        abs_path = os.getcwd().replace("\\", "\\\\")
        graphimport(input, driver, abs_path)
    # if it's a folder, find all the .py files and map all of them
    else:
        # Get the location of the input dir
        # strip if just .
        if input == ".":
            input = ""
        abs_path = os.path.join(os.getcwd(), input).replace("\\", "\\\\")
        files = findpyfiles(input)
        for file in files:
            filepath = file.replace("\\\\", "\\")
            if "site-packages" not in filepath and (abs_path is None or abs_path in filepath):
                # add files as individual nodes
                filename = os.path.basename(filepath).replace(".py", "")
                with driver.session() as session:
                    query = f"MERGE (m:Module {{name: '{filename}', path: '{filepath}'}}) RETURN m"
                    session.run(query)
        for file in files:
            filepath = file.replace("\\\\", "\\")
            graphimport(filepath, driver, abs_path)
    return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        "Correct Usage: python pgs.py [file or directory to map]"
    else:
        graphpyproj(sys.argv[1])