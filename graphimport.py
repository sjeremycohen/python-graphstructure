import ast
import sys
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv


def modfile(imp, name):
    mod = __import__(name)
    try:
        mod_path = mod.__file__
    except AttributeError:
        mod_path = name + " is part of the standard Python library"
    return mod_path


def buildquery(imp, filename, filepath, abs_path=None):
    if isinstance(imp, ast.ImportFrom):
        module = imp.module
        mod_path = modfile(imp, module)
        class_func = ", ".join([alias.name for alias in imp.names])

        query = f"""
            MERGE (m:Module {{name: '{filename}', path: '{filepath}'}})
            MERGE (n {{name: '{module}'}})
            ON CREATE
                SET n:External_Module,
                n.path = '{mod_path}'
            MERGE (m)-[:IMPORTS {{classes_or_functions: '{class_func}'}}]->(n)
            """

    else:
        for n in imp.names:
            module = n.name
            mod_path = modfile(imp, module)
            query = f"""
            MERGE (m:Module {{name: '{filename}', path: '{filepath}'}})
            MERGE (n {{name: '{module}'}})
            ON CREATE
                SET n:External_Module,
                n.path = '{mod_path}'
            MERGE (m)-[:IMPORTS]->(n)
            """
    return query


def graphimport(filepath, driver, abs_path=None):
    filename = os.path.basename(filepath).replace(".py", "")
    if "site-packages" not in filepath and (abs_path is None or abs_path in filepath):
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())

        # Extract the import and import from statements
        imports = [node for node in ast.iter_child_nodes(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        with driver.session() as session:
            query = f"MERGE (m:Module {{name: '{filename}', path: '{filepath}'}}) RETURN m"
            session.run(query)
            for imp in imports:
                query = buildquery(imp, filename, filepath, abs_path)
                session.run(query)
    return


if __name__ == "__main__":
    file = sys.argv[1]
    load_dotenv()
    n4js = os.environ.get('NEO4J_SERVER')
    n4jdb = os.environ.get('NEO4J_DB')
    n4jpw = os.environ.get('NEO4J_PW')
    driver = GraphDatabase.driver(n4js, auth=(n4jdb, n4jpw))
    abs_path = os.getcwd().replace("\\", "\\\\")
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    graphimport(file, driver, abs_path)
