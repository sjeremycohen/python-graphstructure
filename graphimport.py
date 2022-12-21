import ast
import sys
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from findmod import findmod
from findpath import findpath


def graphimport(file, driver, syspaths, abs_path=None):
    filename = os.path.basename(file)
    filepath = findmod(filename, syspaths).replace("\\", "\\\\")
    with open(file, 'r') as f:
        tree = ast.parse(f.read())

    # What if, as an alternative to grabbing filepath, we simply extract the module name from the import string and use that alone? Disadvantage: for Django projects, you can have models.py in multiple folders.

    # Extract the import and import from statements
    imports = [node for node in ast.iter_child_nodes(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    with driver.session() as session:
        query = f"MERGE (m:Module {{name: '{filename}', path: '{filepath}'}}) RETURN m"
        session.run(query)
        for i in imports:
            if isinstance(i, ast.ImportFrom):
                module = i.module
                mod_path = findmod(module, syspaths).replace("\\", "\\\\")
                classes_or_functions = ", ".join([alias.name for alias in i.names])
                print(abs_path + " - " + mod_path)
                if abs_path is not None and abs_path in mod_path:
                    mod_type = "Module"
                else:
                    mod_type = "External_Module"
                query = f"""
                    MERGE (m:Module {{name: '{filename}', path: '{filepath}'}})
                    MERGE (n:{mod_type} {{name: '{module}', path: '{mod_path}'}})
                    ON CREATE
                        SET n.name='{module}'
                    MERGE (m)-[:IMPORTS {{classes_or_functions: '{classes_or_functions}'}}]->(n)
                    """

            else:
                for n in i.names:
                    module = n.name
                    mod_path = findmod(module, syspaths).replace("\\", "\\\\")
                    print(abs_path + " - " + mod_path)
                    if abs_path is not None and abs_path in mod_path:
                        mod_type = "Module"
                    else:
                        mod_type = "External_Module"
                    query = f"""
                    MERGE (m:Module {{name: '{filename}', path: '{filepath}'}})
                    MERGE (n:{mod_type} {{path: '{mod_path}'}})
                    ON CREATE
                        SET n.name='{module}'
                    MERGE (m)-[:IMPORTS]->(n)
                    """
            session.run(query)

if __name__=="__main__":
    file = sys.argv[1]
    load_dotenv()
    n4js = os.environ.get('NEO4J_SERVER')
    n4jdb = os.environ.get('NEO4J_DB')
    n4jpw = os.environ.get('NEO4J_PW')
    driver = GraphDatabase.driver(n4js, auth=(n4jdb, n4jpw))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    graphimport(file, driver, findpath(sys.path))
