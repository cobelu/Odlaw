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
        self.fks = connector.query_fks_sqlite()

        # The database is represented by a graph
        self.graph = nx.MultiDiGraph()

        # Each node is a table in the database
        for table in self.tables:
            self.graph.add_node(table)

        # Each arc is a foreign key constraint
        # for fk in self.fks:
        #     # The head of the arc is the foreign key's table
        #     # The tail of the arc is the primary key's table
        #     # The name of the arc is the name of the FK constraint
        #     from_table = ""
        #     to_table = ""
        #     self.graph.add_edge(from_table, to_table, name="name")

    def plot(self):
        # TODO: Export the graph as a matplotlib plot
        nx.draw(self.graph)
