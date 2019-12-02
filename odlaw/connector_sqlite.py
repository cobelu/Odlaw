from odlaw.connector import Connector

import pandas as pd


class ConnectorSQLite(Connector):

    def __init__(self, db_url):
        Connector.__init__(self, db_url)

    def query_tables(self):
        """
        Asks a SQLite DB for its tables.

        :return: A pandas DF of tables in the SQLite DB
        """
        # Find all tables
        tables_q = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE \'sqlite_%\';"
        tables = self.query(tables_q)
        # print(tables)
        return tables

    def query_pks(self):
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
            # https://www.oreilly.com/library/view/using-sqlite/9781449394592/re176.html
            pks_q = "PRAGMA table_info(%s);" % table
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
        # print(pks)
        return pks

    def query_fks(self):
        """
        Asks a SQLite DB for its foreign keys.

        :return: A pandas DF of foreign keys in the SQLite DB
        """
        # Empty DataFrame to be appended
        fks = pd.DataFrame()

        # Find all tables
        tables = self.query_tables()
        table_names = tables['name'].tolist()
        for table in table_names:
            # https://www.oreilly.com/library/view/using-sqlite/9781449394592/re176.html
            fks_q = "PRAGMA foreign_key_list(%s);" % table
            # Ask for the foreign keys on that table
            fk = self.query(fks_q)
            # Discard non-necessary info
            fk = fk[['table', 'from', 'to']]
            fk['from_table'] = table
            # Append to running log
            fks = fks.append(fk)

        # All found, so reindex and return
        # print(fks)
        return fks
