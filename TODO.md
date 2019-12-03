# Odlaw

This document is a TODO list, note page, and resources guide for the development of Odlaw.


## TODO

* Talk about deletion
    * Deletion should be "rootward" (i.e. nearly identical to the visit method, but deletes after visit and commits after all deletions are successful)
* Connector methods for PGSQL
    * Lookup syntax
* Graves clicking functionality     


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


## Sample Datasets

* [Oracle's Employees MySQL Database](https://dev.mysql.com/doc/employee/en/ "employees")
* [MySQLTutorial's Classic Car Businesses MySQL Database](http://www.mysqltutorial.org/mysql-sample-database.aspx "classicmodels")
* [Lovasoa's Port of TPC-H for SQLite](https://github.com/lovasoa/TPCH-sqlite "TPC-H")
* [SQLiteTutorial's Record Store SQLite Database](https://www.sqlitetutorial.net/sqlite-sample-database/ "chinook")
