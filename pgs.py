import ast
import sys
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from findmod import findmod



def findModule(module_name):
    for path in sys.path:
        full_path = os.path.join(path, module_name.replace('.','/'))
        if os.path.exists(full_path):
            return full_path
    else:
        return 1


def graphImports(file, driver):
    filename = os.path.basename(file)
    with open(file, 'r') as f:
        tree = ast.parse(f.read())

    # What if, as an alternative to grabbing filepath, we simply extract the module name from the import string and use that alone? Disadvantage: for Django projects, you can have models.py in multiple folders.

    # Extract the import and import from statements
    imports = [node for node in ast.iter_child_nodes(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    with driver.session() as session:
        query = "MERGE (m:Module {{name: '{}'}}) RETURN m".format(filename)
        session.run(query)
        for i in imports:
            if isinstance(i, ast.ImportFrom):
                module = i.module
                classes_or_functions = ", ".join([alias.name for alias in i.names])
                query = """
                    MERGE (m:Module {{name: '{}'}})
                    MERGE (n:Module {{name: '{}'}})
                    MERGE (m)-[:IMPORTS {{classes_or_functions: '{}'}}]->(n)
                    """.format(filename, module, classes_or_functions)
                session.run(query)
            else:
                for n in i.names:
                    module = n.name
                    query = """
                        MERGE (m:Module {{name: '{}'}})
                        MERGE (n:Module {{name: '{}'}})
                        MERGE (m)-[:IMPORTS]->(n)
                        """.format(filename, module)
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
    graphImports(file, driver)
