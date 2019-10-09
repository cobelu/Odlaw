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
        for row in result:
            print("username:", row['username'])
        self.connection.close()
