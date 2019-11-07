from sqlalchemy import create_engine
import pandas as pd


class Connector:
    """
    A wrapper around the SQLAlchemy engine and connection to simplify interactions with the database.
    """

    def __init__(self, db_url):
        self.db_name = db_url
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()

    def query(self, query):
        """
        Queries the database.

        :param query: SQL string to be executed
        :return: A pandas DF of the query results
        """
        result = pd.read_sql_query(query, self.engine)
        return result

    def query_for_report(self, table, col, in_values):
        query = "SELECT * FROM %s WHERE %s IN (%s);" % (table, col, in_values)
        # print(query)
        data = self.query(query)
        return data

    def query_tables_pgsql(self):
        """
        Asks a PostgreSQL DB for its tables.

        :return: A pandas DF of tables in the PGSQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        # TODO: Simplify query
        tables_q = "SELECT *"
        tables_q += "FROM pg_catalog.pg_tables"
        tables_q += "WHERE schemaname != \'pg_catalog\'"
        tables_q += "AND schemaname != \'information_schema\';"
        tables = self.query(tables_q)
        return tables

    def query_tables_sqlite(self):
        """
        Asks a SQLite DB for its tables.

        :return: A pandas DF of tables in the SQLite DB
        """
        # Find all tables
        tables_q = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE \'sqlite_%\';"
        tables = self.query(tables_q)
        return tables

    def query_pks_sqlite(self):
        """
        Asks a SQLite DB for its primary keys.

        :return: A dictionary of primary keys in the SQLite DB
        """
        # Empty DataFrame to be appended
        pks = {}

        # Find all tables
        tables = self.query_tables_sqlite()
        table_names = tables['name'].tolist()
        for table in table_names:
            # https://www.oreilly.com/library/view/using-sqlite/9781449394592/re176.html
            pks_q = "PRAGMA table_info(%s);" % table
            # Ask for the foreign keys on that table
            pk = self.query(pks_q)
            # Discard non-necessary info
            pk = pk[pk['pk'] == 1]['name'].values[0]
            # Append to running log
            pks[table] = pk

        # All found, so reindex and return
        return pks

    def query_fks_sqlite(self):
        """
        Asks a SQLite DB for its foreign keys.

        :return: A pandas DF of foreign keys in the SQLite DB
        """
        # Empty DataFrame to be appended
        fks = pd.DataFrame()

        # Find all tables
        tables = self.query_tables_sqlite()
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
        return fks

    def close(self):
        """
        Closes the connection to the database.
        Should be called when all work is done, every time.

        :return: None
        """
        self.connection.close()
        return
