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
        self.verbose = False

    def query(self, query):
        """
        Queries the database.
        NOTE THAT THIS METHOD SHOULD NEVER (EVER) BE CALLED.
        It should ONLY be used as a helper method within this class.

        :param query: SQL string to be executed
        :return: A pandas DF of the query results
        """
        if self.verbose:
            print(query)
        result = pd.read_sql_query(query, self.engine)
        return result

    def query_for_report(self, table, col, in_values):
        """
        Queries the database for generation of a report.

        :param table: The table to query
        :param col: The foreign key column of the previous table
        :param in_values: The values from the previous table that are of interest
        :return: A pandas DF of table entries of in_values
        """
        query = "SELECT * FROM %s WHERE %s IN (%s);" % (table, col, in_values)
        # print(query)
        data = self.query(query)
        return data

    def query_for_deletion(self, table, col, in_values):
        """
        DANGER: Very dangerous method.
        Helps to remove sub-table data from the database.

        :param table: The table to delete from
        :param col: The primary key column of the table
        :param in_values: The values from the table that are flagged for deletion
        :return: Result of deletion
        """
        query = "DELETE FROM %s WHERE %s IN (%s);" % (table, col, in_values)
        print(query)
        self.engine.execute(query)
        return

    def close(self):
        """
        Closes the connection to the database.
        Should be called when all work is done, every time.

        :return: None
        """
        self.connection.close()
        return
