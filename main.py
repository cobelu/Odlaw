# Odlaw
# Retroactive GDPR compliance for rendering exports of user data

from connector import Connector
from database import Database
import psycopg2
import argparse


def main():

    # Pull database connection information from the inputs
    # dialect+driver://username:password@host:port/database

    # https://stackabuse.com/command-line-arguments-in-python/
    # initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dialect", type=str, default='sqlite', help='SQL dialect', action='store')
    parser.add_argument("-r", "--driver", type=str, default='psycopg2', help='Driver', action='store')
    parser.add_argument("-u", "--user", type=str, default='', help='Username', action='store')
    parser.add_argument("-P", "--password", type=str, default='', help='Password', action='store')
    parser.add_argument("-H", "--host", type=str, default='localhost', help='Host', action='store')
    parser.add_argument("-p", "--port", type=int, default=5432, help='Port', action='store')
    parser.add_argument("-n", "--name", type=str, default='', help='Database name', action='store')
    parser.add_argument("-V", "--version", help='Show program version', action='store_true')

    # read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    if args.version:
        print("Odlaw v0.1")

    # Other command line args
    plot = ''  # Location of plot

    # Build up a database URL
    # url = "%s+%s://%s:%s@%s:%s/%s" % (args.dialect,
    #                                   args.driver,
    #                                   args.user,
    #                                   args.password,
    #                                   args.host,
    #                                   args.port,
    #                                   args.name)

    # Testing URL
    url = 'sqlite:///company.db'

    # Generate a connection
    connector = Connector(url)

    # Create a graph representation of the database
    database = Database(connector)
    print(database.tables)
    print(database.fks)

    # Generate visual graph representation (if desired)

    # Don't forget to close the connection when done!
    connector.close()


if __name__ == '__main__':
    main()
