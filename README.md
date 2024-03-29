![Odlaw](docs/resources/odlaw_logo.png)

# Odlaw

Odlaw is a client to look for and help delete customer data in relational databases for GDPR compliancy.


## Setup
* You'll need to install the dependencies listed out in requirements.txt, preferably in a Python virtual environment
* To activate the virtual environment run:

    `source venv/bin/activate`

  From the root of the project. The string (venv) should be prepended to the terminal prompt if the virtual environment was activated correctly.
* Then, to install the required packages, run:

    `pip3 install -r requirements.txt`

  Also from the root of the project. To install the packages on only the virtual environment (and not the system one), make sure
that the virtual environment is set up correctly first through the command above. Otherwise, if you want the packages to be installed
system-wide, then simply run the command above without the virtual environment.


## Usage

* `-d/--dialect` - The dialect of the database. Valid options are `SQLite` or `MySQL` (non-case-sensitive).
* `-r/--driver` - Specifies the driver (currently non-functional)
* `-u/--user` - Username for database access.
* `-p/--password` - Password for database access.
* `-H/--host` - Hostname for database access.
* `-P/--port` - Port for database access.
* `-m/--measure` - Appends {ID, time (ns)} to log file (CSV) for operation timing
* `-n/--name` - Name of the database (required).
* `-R/--report` - Flag to determine if a report should be generated.
* `-t/--table` - Name of the table from which the search should start (i.e., the User table).
* `-i/--identifier` - Unique identifier of the User for which the report/deletion should affect.
* `-o/--output` - Filepath to where the report should be stored (if `--report` is set).  
* `-b/--block` - A comma-delimited list of `<TABLE>.<COLUMN>` which should be excluded from the report.
* `-c/--censor` - Boolean. Censors primary keys from the report. 
* `-x/--delete` - Boolean. Used in place of `--report` if a user and their data should be deleted. 
* `-s/--show` - Boolean. Shows the graphical form of the database. 
* `-j/--joined` - Boolean. Prints connected components of database.
* `-v/--verbose` - Boolean. Prints all queries to console for debugging. 
* `-V/--version` - Boolean. Prints version.
* `-h/--help` - Boolean. Prints help.


## Examples

* SQLite Graph for TPC-H:
    * `python3 main.py -d sqlite -n samples/sqlite/TPC-H-small.db -s -j`
* SQLite Search for TPC-H:
    * `python3 main.py -d sqlite -n samples/sqlite/TPC-H-small.db -s -j`    
* MySQL Search in Employees:
    * `python3 main.py -d mysql -u <Username> -p <Password> -n employees -R -t employees -i 10001`
* MySQL Deletion of an Employee in Employees
    * `python3 main.py -d mysql -u <Username> -p <Password> -n employees -x -t employees -i 10001` 


## Sample Databases

### SQLite
* [SQLiteTutorial.net's Sample Database](https://www.sqlitetutorial.net/sqlite-sample-database/ "chinook")
* [TPC-H in SQLite](https://github.com/lovasoa/TPCH-sqlite "SQLite TPC-H")

### MySQL
* [Oracle's Employee Sample Database](https://dev.mysql.com/doc/employee/en/ "employees")
* [MySQLTutorial.org's Sample Database](http://www.mysqltutorial.org/mysql-sample-database.aspx "classicmodels")
* [HotCRP](https://github.com/kohler/hotcrp/blob/master/src/schema.sql "HotCRP")

