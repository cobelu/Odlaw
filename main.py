# Odlaw
# Retroactive GDPR compliance for rendering exports of user data

from odlaw.connector_mysql import ConnectorMySQL
from odlaw.connector_pgsql import ConnectorPostgreSQL
from odlaw.connector_sqlite import ConnectorSQLite
from odlaw.database import Database

from urllib.parse import quote_plus
import argparse
import time


def main():
    # Pull database connection information from the inputs
    # dialect+driver://username:password@host:port/database

    # https://stackabuse.com/command-line-arguments-in-python/
    # initiate the parser
    parser = argparse.ArgumentParser()
    # Database connection options
    parser.add_argument("-d", "--dialect", type=str, default='sqlite', help='SQL dialect', action='store')
    parser.add_argument("-r", "--driver", type=str, help='Driver', action='store')
    parser.add_argument("-u", "--user", type=str, help='Username', action='store')
    parser.add_argument("-P", "--password", type=str, help='Password', action='store')
    parser.add_argument("-H", "--host", type=str, help='Host', action='store')
    parser.add_argument("-p", "--port", type=int, help='Port', action='store')
    parser.add_argument("-n", "--name", type=str, default='sqlite/TPC-H-small.db', help='Database name', action='store', required=True)

    # Report generation
    parser.add_argument("-R", "--report", help='Generates a report', action='store_true')
    parser.add_argument("-t", "--table", type=str, help='User table name', action='store')
    parser.add_argument("-i", "--identifier", type=int, help='Unique user identifier for report', action='store')
    parser.add_argument("-o", "--output", type=str, help='Directory to place the report', action='store')
    parser.add_argument("-b", "--block", type=str, help='''
        Comma-delimited list of columns which should not be included in the report
        in <TABLE>.<COLUMN> format''', action='store')
    parser.add_argument("-c", "--censor", type=str, help='Removes primary key columns from report', action='store')

    # Deletion
    parser.add_argument("-x",
                        "--remove",
                        help='Removes a user and all dependent data from the database',
                        action='store_true')

    # Plotting
    parser.add_argument("-s", "--show", action='store_true')

    # Health
    parser.add_argument("-j", "--joined", action='store_true')

    # Application
    parser.add_argument("-m", "--measure", type=str,
                        help='If command should be measured and where the *.csv file should be stored',
                        action='store')
    parser.add_argument("-v", "--verbose", help='Displays all queries', action='store_true')
    parser.add_argument("-V", "--version", help='Show program version', action='store_true')

    # read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    if args.version:
        print("Odlaw v0.1")

    # Url structure
    # dialect+driver://username:password@host:port/database

    # Example postgres
    # postgresql://scott:tiger@localhost/mydatabase
    # postgresql+psycopg2://scott:tiger@localhost/mydatabase

    # Begin timing
    start = time.time_ns()

    # Build up a database URL
    url = args.dialect
    if args.driver:
        url += ';+%s' % args.driver
    if args.dialect.lower() == 'mysql':
        url += '+pymysql'
    url += '://'
    if args.user:
        # Usernames can hold url-unfriendly chars
        url += quote_plus(args.user)
        if args.password:
            # Passwords can hold url-unfriendly chars
            url += ':%s' % quote_plus(args.password)
        url += '@'
        if args.host:
            url += '%s' % args.host
        else:
            url += 'localhost'
        if args.port:
            url += ':%s' % args.port

    url += '/%s' % args.name

    # Testing URL
    # url = 'sqlite:///sqlite/TPC-H-small.db'

    # Print the URL (DEV)
    # print(url)

    # Generate a connection
    if args.dialect.lower() == "mysql":
        connector = ConnectorMySQL(url, args.name)
    elif args.dialect.lower() == "postgresql":
        connector = ConnectorPostgreSQL(url, args.name)
    elif args.dialect.lower() == "sqlite":
        connector = ConnectorSQLite(url)
    else:
        raise Exception("Invalid dialect")

    # Tell the connector to be verbose
    if args.verbose:
        connector.verbose = True

    # Create a graph representation of the database
    database = Database(connector)

    # Generate a health check-up (if desired)
    if args.joined:
        if database.is_connected():
            print("Database is connected. Each table is connected to some other table via a foreign key.")
        else:
            print("Database is NOT connected.")
            print("Consider connecting the connected components:")
            components = database.connected_components()
            for component in components:
                print(component)

    # Generate visual graph representation (if desired)
    if args.show:
        database.plot()

    # Generate report and save (if desired)
    if args.report and args.table and args.identifier and args.output:
        database.generate_csv_user_data_report(args.table, args.identifier, args.report)
    elif args.report and args.table and args.identifier:
        report = database.generate_user_data_report(args.table, args.identifier)
        report.print_report()

    # Deletion (if desired)
    if args.remove and args.table and args.identifier:
        response = input("Are you sure that you want to remove User %s? [Y]es/[No]: " % args.identifier)
        response = response.lower()
        if response == "y" or response == "yes":
            database.remove_user(args.table, args.identifier)
            print("User %s removed" % args.identifier)
        elif response == "n" or response == "no":
            print("User %s was NOT removed" % args.identifier)
        else:
            print("ERROR: Please try again")
    elif args.remove:
        print("Please specify table and identifier")

    # Write measured time to file
    if args.measure and args.identifier:
        stop = time.time_ns()
        elapsed_time = stop - start
        with open(args.measure, "a") as output:
            output.write("%s,%d\n" % (args.identifier, elapsed_time))

    # Don't forget to close the connection when done!
    connector.close()


if __name__ == '__main__':
    main()
