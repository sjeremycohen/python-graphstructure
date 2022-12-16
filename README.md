# python-graphstructure
Graph the relationships between Python files within a project/directory.

Inspired by Kasper Müller (though all used code is written from scratch); originally documented in [this medium post](https://towardsdatascience.com/building-a-map-of-your-python-project-using-graph-technology-visualize-your-code-6764e81f3500)

## Requirements
1. An active [Neo4J](https://neo4j.com/) server - (only tested on Local, but there's no reason this shouldn't work with Aura!)
2. Any Python project (even this one!)
3. A curious mind!

## How To Use
1. Set up your Neo4J server (you can find instructions on how to do this on their site)
2. Clone or Download this repo
3. Within the root dir of the repo, create a file called `.env`
4. Fill out `.env` as follows
    ```
    NEO4J_SERVER=[your Neo4j server url]
    NEO4J_DB=[your db name]
    NEO4J_PW=[your db pw]
    ```
5. Install the requirements (I recommend using a [virtual environment](https://docs.python.org/3/library/venv.html), though this is not required):
6. ```
   pip install -r requirements.txt
   ```
7. Open a terminal in the project directory
8. Run like this:
    ```
    python pgs.py [file or directory to map]
    ```