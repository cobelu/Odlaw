from sqlalchemy.engine import create_engine


class Connector:
    """
    A wrapper around the SQLAlchemy engine and connection to simplify interactions with the database.
    """

    def __init__(self, db_url):
        self.db_name = db_url
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()

    def query(self, query):
        result = self.connection.execute(query)
        return result

    def query_tables(self):
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        # TODO: Simplify query
        tables_q = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
        tables = self.query(tables_q)
        return tables

    def query_fks(self):
        fks = self.query("SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE='FOREIGN KEY';")
        # TODO: Figure out HOW schema is stored
        # TODO: Figure out HOW to store fks after we know what it is (needs easy import in Database)
        return fks

    def close(self):
        self.connection.close()
