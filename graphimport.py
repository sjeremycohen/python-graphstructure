import ast
import sys
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from findmod import findmod
from findpath import findpath


def buildquery(imp, filename, filepath, syspaths, abs_path=None):
    if isinstance(imp, ast.ImportFrom):
        module = imp.module
        mod_path = findmod(module, syspaths).replace("\\", "\\\\")
        class_func = ", ".join([alias.name for alias in imp.names])
        print(abs_path + " - " + mod_path)
        if abs_path is not None and abs_path in mod_path and ("site-packages" not in mod_path):
            mod_type = "Module"
        else:
            mod_type = "External_Module"
        query = f"""
            MERGE (m:Module {{name: '{filename}', path: '{filepath}'}})
            MERGE (n:{mod_type} {{name: '{module}', path: '{mod_path}'}})
            ON CREATE
                SET n.name='{module}'
            MERGE (m)-[:IMPORTS {{classes_or_functions: '{class_func}'}}]->(n)
            """

    else:
        for n in imp.names:
            module = n.name
            mod_path = findmod(module, syspaths).replace("\\", "\\\\")
            print(abs_path + " - " + mod_path)
            if abs_path is not None and abs_path in mod_path and ("site-packages" not in mod_path):
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
    return query


def graphimport(file, driver, syspaths, abs_path=None):
    filename = os.path.basename(file).replace(".py", "")
    filepath = findmod(filename, syspaths).replace("\\", "\\\\")
    if "site-packages" not in filepath and (abs_path is None or abs_path in filepath):
        with open(file, 'r') as f:
            tree = ast.parse(f.read())

        # Extract the import and import from statements
        imports = [node for node in ast.iter_child_nodes(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        with driver.session() as session:
            query = f"MERGE (m:Module {{name: '{filename}', path: '{filepath}'}}) RETURN m"
            session.run(query)
            for imp in imports:
                query = buildquery(imp, filename, filepath, syspaths, abs_path)
                session.run(query)
    return


if __name__ == "__main__":
    file = sys.argv[1]
    load_dotenv()
    n4js = os.environ.get('NEO4J_SERVER')
    n4jdb = os.environ.get('NEO4J_DB')
    n4jpw = os.environ.get('NEO4J_PW')
    driver = GraphDatabase.driver(n4js, auth=(n4jdb, n4jpw))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    graphimport(file, driver, findpath(sys.path))
