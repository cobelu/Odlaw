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
        result = pd.read_sql_query(query, self.engine)
        return result

    def query_tables_pgsql(self):
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        # TODO: Simplify query
        tables_q = "SELECT *"
        tables_q += "FROM pg_catalog.pg_tables"
        tables_q += "WHERE schemaname != \'pg_catalog\'"
        tables_q += "AND schemaname != \'information_schema\';"
        tables = self.query(tables_q)
        return tables

    def query_tables_sqlite(self):
        # Find all tables
        tables_q = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE \'sqlite_%\';"
        tables = self.query(tables_q)
        return tables

    def query_fks_sqlite(self):
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
            # Append to running log
            fks = fks.append(fk)

        # All found, so return now
        return fks

    def close(self):
        self.connection.close()
