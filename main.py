# Odlaw
# Retroactive GDPR compliance for rendering exports of user data

from odlaw.connector import Connector
from odlaw.database import Database
from urllib.parse import quote_plus
import argparse


def main():

    # Pull database connection information from the inputs
    # dialect+driver://username:password@host:port/database

    # https://stackabuse.com/command-line-arguments-in-python/
    # initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dialect", type=str, default='sqlite', help='SQL dialect', action='store')
    parser.add_argument("-r", "--driver", type=str, help='Driver', action='store')
    parser.add_argument("-u", "--user", type=str, help='Username', action='store')
    parser.add_argument("-P", "--password", type=str, help='Password', action='store')
    parser.add_argument("-H", "--host", type=str, help='Host', action='store')
    parser.add_argument("-p", "--port", type=int, help='Port', action='store')
    parser.add_argument("-n", "--name", type=str, default='/sqlite/TPC-H-small.db', help='Database name', action='store')
    parser.add_argument("-V", "--version", help='Show program version', action='store_true')

    # read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    if args.version:
        print("Odlaw v0.1")

    # Other command line args
    plot = ''  # Location of plot

    # dialect+driver://username:password@host:port/database

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
            url += args.host
        else:
            print("Username provided, but not host. Defaulting to host to 'localhost'")
            url += 'localhost'
        if args.port:
            url += ':%s' % args.port
    url += args.name

    # Testing URL
    # url = 'sqlite:///sqlite/TPC-H-small.db'

    # Generate a connection
    connector = Connector(url)

    # Create a graph representation of the database
    database = Database(connector)

    # print(database.graph.nodes)
    # sample_report = database.generate_user_data_report('CUSTOMER', 6)
    # for table in sample_report.tables:
    #     values = sample_report.tables.get(table)
    #     print("\t" + table)
    #     print(values)

    # Generate visual graph representation (if desired)
    # database.plot()

    # print(database.connector.query_pks_sqlite())
    # report = database.generate_csv_user_data_report('CUSTOMER', 4)
    report = database.generate_csv_user_data_report('CUSTOMER', 4, "csv")
    print("-" * 25)
    # print(report.tables['CUSTOMER'])
    # print(report.tables['ORDERS'])
    # print(report.tables['LINEITEM'])

    # Don't forget to close the connection when done!
    connector.close()


if __name__ == '__main__':
    main()
