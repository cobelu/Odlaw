# Odlaw
# Retroactive GDPR compliance for rendering exports of user data

import sys
from connector import Connector
from database import Database


def main():

    # Pull database connection information from the inputs
    # dialect+driver://username:password@host:port/database
    dialect = ''
    driver = ''
    username = ''
    password = ''
    host = ''
    port = ''
    database = ''

    # Other command line args
    plot = ''  # Location of plot

    # Build up a database URL
    url = f'{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'

    # Generate a connection
    connector = Connector(url)

    # Create a graph representation of the database
    database = Database(connector)

    # Generate visual graph representation (if desired)
    if plot:
        database.plot()

    # Don't forget to close the connection when done!
    connector.close()


if __name__ == '__main__':
    main()
