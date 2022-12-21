import os
import sys
import fnmatch
from neo4j import GraphDatabase
from dotenv import load_dotenv

def gitignore_clean(lst):
  return [s for s in lst if s and not s.startswith("#")]

if __name__=="__main__":
    # Import env vars
    load_dotenv()
    env = os.environ

    # Create a Neo4j driver to connect to the database
    n4js = os.environ.get('NEO4J_SERVER')
    n4jdb = os.environ.get('NEO4J_DB')
    n4jpw = os.environ.get('NEO4J_PW')

    driver = GraphDatabase.driver(n4js, auth=(n4jdb, n4jpw))

    # Clear the current neo4j graph
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    # Specify the directory to search
    root_dir = sys.argv[1]

    # Read the .gitignore file and extract the patterns
    with open('.gitignore', 'r') as f:
        patterns = gitignore_clean(f.read().splitlines())
    
    print(patterns)


    # Create a dictionary to store the node ID of each directory
    dir_nodes = {}

    # Loop through all subdirectories in the root directory
    for root, dirs, files in os.walk(root_dir):
        # Create a Neo4j session
        with driver.session() as session:
            # Get the directory name and parent directory path
            dir_name = os.path.basename(root)
            parent_path = os.path.dirname(root)
            if any(fnmatch.fnmatch(dir_name, pattern) for pattern in patterns):
                print("gitignore match: " + dir_name)
                continue
            # Create a query to create the directory node
            query = """
                CREATE (d:Directory {{name: '{}'}})
                RETURN d
            """.format(dir_name)

            # Execute the query and store the directory node
            dir_node = session.run(query).single()[0]
            dir_nodes[root] = dir_node

            # If the directory has a parent directory, create a relationship
            if parent_path in dir_nodes:
                parent_node = dir_nodes[parent_path]
                session.run("MATCH (p:Directory), (c:Directory) "
                            "WHERE p.name = '{}' AND c.name = '{}' "
                            "CREATE (p)-[:CHILD]->(c)".format(parent_node['name'], dir_node['name']))

        # Loop through all files in the current directory
        for file in files:
            if not file.endswith(".py"):
                continue
            if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                print("gitignore match: " + file)
                continue
            # Create a Neo4j session
            with driver.session() as session:
                # Create a query to create the file node
                query = """
                    CREATE (f:File {{name: '{}'}})
                    RETURN f
                """.format(file)

                # Execute the query and store the file node
                file_node = session.run(query).single()[0]

                # Create a relationship between the file and its directory
                session.run("MATCH (d:Directory), (f:File) "
                            "WHERE d.name = '{}' AND f.name = '{}' "
                            "CREATE (d)-[:CONTAINS]->(f)".format(dir_node['name'], file_node['name']))

    # Close the Neo4j driver
    driver.close()