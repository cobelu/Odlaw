# Odlaw

Odlaw is a client to look for and help delete customer data in relational databases for GDPR compliancy.

## TODO

* The generate_csv_user_data_report method generates a dictionary of table name keys with pandas DF values
    *  Use [pandas' to_csv function on each DF in the dict (values) to store to a folder](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html "DF to_csv")
* Talk about deletion
    * Deletion should be "rootward" (i.e. nearly identical to the visit method, but deletes after visit and commits after all deletions are successful)
* Command line args
* Connector methods for PGSQL
    * Lookup syntax
* Add a "healthiness" feature (-h?) that [checks if the graph is connected](https://networkx.github.io/documentation/stable/reference/algorithms/component.html "NetworkX Components") (all foreign keys are present) in orrder to determine health and suggest connections.

## Notes

* SQLAlchemy uses `dialect+driver://username:password@host:port/database` as a format, so we'll want to use an arg parser to figure out the optional inputs
* Each node represents a table in a database
* Each arc represents a foreign key entry in a table (tail) to a primary key in another table (source)
* The label of each arc is the name of the foreign key constraint (DBAs are _supposed_ to name their key constraints)

## Help

* You'll want to install PostgreSQL and pgAdmin on your box
* [Read this tutorial to get started](https://www.datacamp.com/community/tutorials/beginners-introduction-postgresql "PostgreSQL Tutorial")
* [NetworkX Docs are here](https://networkx.github.io/documentation/stable/index.html "NetworkX Docs")
* [We may/will have parallel edges, so we will need a MultiDiGraph](https://networkx.github.io/documentation/stable/reference/classes/multidigraph.html "MultiDiGraph")
* [It would be best to automatically generate a graph from one of the built-in functions (faster), but I had some problems with this before](https://networkx.github.io/documentation/stable/reference/convert.html "Convert")
* [It would be best to automatically generate a graph from one of the built-in functions (faster), but I had some problems with this before](https://networkx.github.io/documentation/stable/reference/convert.html "Convert")
* [We should think about drawing the graphs, so DBAs can verify there exist foreign keys (Matplotlib is fine)](https://networkx.github.io/documentation/stable/reference/drawing.html "Drawing NetworkX Graphs")
