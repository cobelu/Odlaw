from odlaw.connector import Connector

import pandas as pd


class ConnectorMySQL(Connector):

    def __init__(self, db_url, database):
        Connector.__init__(self, db_url)
        self.database = database

    def query_tables(self):
        """
        Asks a MySQL DB for its tables.

        :return: A pandas DF of tables in the MySQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        tables_q = "SELECT table_name "
        tables_q += "FROM information_schema.tables "
        tables_q += "WHERE table_schema=\'%s\';" % self.database
        tables = self.query(tables_q)

        # Rename the column name for compatibility
        tables = tables.rename(columns={'TABLE_NAME': 'name'})

        return tables

    def query_pks(self):
        """
        Asks a MySQL DB for its primary keys.

        :return: A pandas DF of primary keys in the MySQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        """
        Asks a MySQL DB for its primary keys.

        :return: A dictionary of primary keys in the SQLite DB
        """
        # Empty DataFrame to be appended
        pks = {}

        # Find all tables
        tables = self.query_tables()
        table_names = tables['name'].tolist()
        for table in table_names:
            pks_q = "SHOW KEYS FROM %s WHERE Key_name=\'PRIMARY\'" % table
            # Ask for the primary keys on that table
            pk = self.query(pks_q)
            # Discard non-necessary info
            try:
                pk = pk[pk['Non_unique'] == 0]['Column_name'].values[0]
            # If there are no primary keys for the table
            except IndexError:
                pk = pd.DataFrame()
            # Append to running log
            pks[table] = pk
        # All found, so reindex and return
        print("PRIMARY KEYS:")
        print(pks)
        return pks

    def query_fks(self):
        """
        Asks a MySQL DB for its foreign keys.

        :return: A pandas DF of foreign keys in the MySQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        fks_q = "SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, "
        fks_q += "REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME "
        fks_q += "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
        fks_q += "WHERE TABLE_SCHEMA=\'%s\' AND " % self.database
        fks_q += "REFERENCED_TABLE_NAME IS NOT NULL AND "
        fks_q += "REFERENCED_COLUMN_NAME IS NOT NULL"
        fks = self.query(fks_q)

        # Rename the DF columns
        fks = fks.rename(columns={
            'TABLE_NAME': 'from_table',
            'COLUMN_NAME': 'from',
            'REFERENCED_TABLE_NAME': 'table',
            'REFERENCED_COLUMN_NAME': 'to',
            'CONSTRAINT_NAME': 'name'
        })

        # Return the column of table names in the format
        print(fks)
        return fks
