# Odlaw

Odlaw is a client to look for and help delete customer data in relational databases for GDPR compliancy.

## To Do

* You'll want to install PostgreSQL and pgAdmin on your box
* [Read this tutorial to get started](https://www.datacamp.com/community/tutorials/beginners-introduction-postgresql "PostgreSQL Tutorial")
* [NetworkX Docs are here](https://networkx.github.io/documentation/stable/index.html "NetworkX Docs")
* [We may/will have parallel edges, so we will need a MultiDiGraph](https://networkx.github.io/documentation/stable/reference/classes/multidigraph.html "MultiDiGraph")
* [It would be best to automatically generate a graph from one of the built-in functions (faster), but I had some problems with this before](https://networkx.github.io/documentation/stable/reference/convert.html "Convert")
* [It would be best to automatically generate a graph from one of the built-in functions (faster), but I had some problems with this before](https://networkx.github.io/documentation/stable/reference/convert.html "Convert")
* [We should think about drawing the graphs, so DBAs can verify there exist foreign keys (Matplotlib is fine)](https://networkx.github.io/documentation/stable/reference/drawing.html "Drawing NetworkX Graphs")
* The algorithm for rendering a user data view:
    1. search-for-user-data(from-table, to-table, id, from, to):
        2. results = `SELECT * FROM to-table WHERE from-table.from = to-table.to`
        3. new-id = PK(results)
        4. BFS from new-from-table to each new-to-table:
            5. new-from-col = edge.from-col
            6. new-to-col = edge.to-col
            7. search-for-user-data(new-from-table, new-to-table, id, new-from-col, new-to-col)


## Notes

* SQLAlchemy uses `dialect+driver://username:password@host:port/database` as a format, so we'll want to use an arg parser to figure out the optional inputs
* Each node represents a table in a database
* Each arc represents a foreign key entry in a table (tail) to a primary key in another table (source)
* The label of each arc is the name of the foreign key constraint (DBAs are _supposed_ to name their key constraints)
