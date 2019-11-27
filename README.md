# Odlaw

Odlaw is a client to look for and help delete customer data in relational databases for GDPR compliancy.

# Setup
* You'll need to install the dependencies listed out in requirements.txt, preferably in a Python virtual environment
* To activate the virtual environment run:

    `source venv/bin/activate`

  From the root of the project. The string (venv) should be prepended to the terminal prompt if the virtual environment was activated correctly.
* To then install the required packages, run:

    `pip3 install -r requirements.txt`

  Also from the root of the project. To install the packages on only the virtual environment (and not the system one), make sure
that the virtual environment is set up correctly first through the command above. Otherwise, if you want the packages to be installed
system-wide, then simply run the command above without the virtual environment.

## TODO

* Talk about deletion
    * Deletion should be "rootward" (i.e. nearly identical to the visit method, but deletes after visit and commits after all deletions are successful)
* Connector methods for PGSQL
    * Lookup syntax
* Graves clicking functionality     

# Examples
* SQLite Graph for TPC-H:
    * `python3 main.py -d sqlite -n samples/sqlite/TPC-H-small.db -s -c`
* SQLite Search for TPC-H:
    * `python3 main.py -d sqlite -n samples/sqlite/TPC-H-small.db -s -c`    
* MySQL Search in Employees:
    * `python3 main.py -d mysql -u <Username> -P <Password> -n employees -R -t employees -i 10001`

## Notes

* SQLAlchemy uses `dialect+driver://username:password@host:port/database` as a format, so we'll want to use an arg parser to figure out the optional inputs
* Each node represents a table in a database
* Each arc represents a foreign key entry in a table (tail) to a primary key in another table (source)
* The label of each arc is the name of the foreign key constraint (DBAs are _supposed_ to name their key constraints)
* `python3 main.py -d mysql -u root -P <Password> -n classicmodels`

## Help

* You'll want to install PostgreSQL and pgAdmin on your box
* [Read this tutorial to get started](https://www.datacamp.com/community/tutorials/beginners-introduction-postgresql "PostgreSQL Tutorial")
* [NetworkX Docs are here](https://networkx.github.io/documentation/stable/index.html "NetworkX Docs")
* [We may/will have parallel edges, so we will need a MultiDiGraph](https://networkx.github.io/documentation/stable/reference/classes/multidigraph.html "MultiDiGraph")
* [It would be best to automatically generate a graph from one of the built-in functions (faster), but I had some problems with this before](https://networkx.github.io/documentation/stable/reference/convert.html "Convert")
* [It would be best to automatically generate a graph from one of the built-in functions (faster), but I had some problems with this before](https://networkx.github.io/documentation/stable/reference/convert.html "Convert")
* [We should think about drawing the graphs, so DBAs can verify there exist foreign keys (Matplotlib is fine)](https://networkx.github.io/documentation/stable/reference/drawing.html "Drawing NetworkX Graphs")
