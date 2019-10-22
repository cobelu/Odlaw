import networkx as nx
import pandas as pd


class Database:
    """
    A representation of a database as a graph.
    """

    def __init__(self, connector):

        # Initialize member variables
        self.connector = connector

        # Query for table names
        self.tables = connector.query_tables_sqlite()

        # Query for foreign keys
        # TODO: FIXME
        # self.fks = connector.query_fks_sqlite()

        # TODO: initialize a graph object from networkx from the given connector object
        self.graph = nx.MultiDiGraph()
        # The database is represented by a graph
        # Each node is a table in the database
        # Each arc is a foreign key constraint
        # The name of the arc is the name of the FK constraint
        # The head of the arc is the foreign key's table
        # The tail of the arc is the primary key's table

    def plot(self):
        # TODO: Export the graph as a matplotlib plot
        nx.draw(self.graph)
