# Odlaw
# Retroactive GDPR compliance for rendering exports of user data

from odlaw.connector import Connector
from odlaw.database import Database
from urllib.parse import quote_plus
import argparse
import os


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
    parser.add_argument("-n", "--name", type=str, default='sqlite/TPC-H-small.db', help='Database name', action='store')
    # Report generation
    parser.add_argument("-R", "--report", type=str, default='~', help='Generates a CSV report', action='store')
    parser.add_argument("-t", "--table", type=str, help='User table name', action='store')
    parser.add_argument("-i", "--identifier", type=int, help='Unique user identifier for report', action='store')
    # Plotting
    parser.add_argument("-s", "--show", action='store_true')
    # Health
    # TODO: Implement connection info in Database class
    parser.add_argument("-c", "--connected", action='store_true')
    # Application
    parser.add_argument("-V", "--version", help='Show program version', action='store_true')

    # read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    if args.version:
        print("Odlaw v0.1")

    # Other command line args
    plot = ''  # Location of plot

    # Url structure
    # dialect+driver://username:password@host:port/database

    # Example postgres
    # postgresql://scott:tiger@localhost/mydatabase
    # postgresql+psycopg2://scott:tiger@localhost/mydatabase

    # Build up a database URL
    url = args.dialect
    if args.driver:
        url += ';+%s' % args.driver
    url += '://'
    if args.user:
        # Usernames can hold url-unfriendly chars
        url += quote_plus(args.user)
        if args.password:
            # Passwords can hold url-unfriendly chars
            url += ':%s' % quote_plus(args.password)
        url += '@'
        if args.host:
            url += '%s/' % args.host
        else:
            print("Username provided, but not host. Defaulting to host to 'localhost'")
            url += 'localhost'
        if args.port:
            url += ':%s' % args.port

    url += '/%s' % args.name

    # Testing URL
    url = 'sqlite:///sqlite/TPC-H-small.db'

    print(url)
    # Generate a connection
    connector = Connector(url)

    # Create a graph representation of the database
    database = Database(connector)

    # Generate visual graph representation (if desired)
    if args.show:
        database.plot()

    # Generate report and save (if desired)
    if (args.report is '') and args.table and args.identifier:
        report = database.generate_user_data_report(args.table, args.identifier)
        for entry in report:
            print(entry)
    elif args.report and args.table and args.identifier:
        print(database.generate_csv_user_data_report(args.table, args.identifier, args.report))

    # Don't forget to close the connection when done!
    connector.close()


if __name__ == '__main__':
    main()
