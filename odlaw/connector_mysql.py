from odlaw.connector import Connector

import pandas as pd


class ConnectorMySQL(Connector):

    def __init__(self, database):
        super().__init__(self)
        self.database = database

    @classmethod
    def query_tables(cls):
        """
        Asks a MySQL DB for its tables.

        :return: A pandas DF of tables in the MySQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        # TODO: Fill in database name
        tables_q = "SELECT table_name FROM information_schema.tables"
        tables_q += " WHERE table_schema = \'your_database_name\';"
        tables = cls.query(tables_q)
        # Return the column of table names
        tables = tables['table_name']
        return tables

    @classmethod
    def query_pks_mysql(self):
        """
        Asks a MySQL DB for its primary keys.

        :return: A pandas DF of primary keys in the MySQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        """
        Asks a SQLite DB for its primary keys.

        :return: A dictionary of primary keys in the SQLite DB
        """
        # Empty DataFrame to be appended
        pks = {}

        # Find all tables
        tables = self.query_tables()
        table_names = tables['name'].tolist()
        for table in table_names:
            pks_q = "SHOW KEYS FROM %s WHERE Key_name=\'PRIMARY\'" % table
            # Ask for the foreign keys on that table
            pk = self.query(pks_q)
            # Discard non-necessary info
            try:
                pk = pk[pk['pk'] == 1]['name'].values[0]
            except IndexError:
                pk = pd.DataFrame()
            # Append to running log
            pks[table] = pk

        # All found, so reindex and return
        return pks

    @classmethod
    def query_fks_mysql(self):
        """
        Asks a MySQL DB for its foreign keys.

        :return: A pandas DF of foreign keys in the MySQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        # TODO: Fill in database and table
        tables_q = "SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME "
        tables_q += "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
        tables_q += "WHERE REFERENCED_TABLE_SCHEMA=\'<database>\' AND REFERENCED_TABLE_NAME=\'<table>\';"
        tables = self.query(tables_q)
        # Return the column of table names in the format

        return tables
