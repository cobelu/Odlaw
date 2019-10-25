import matplotlib.pyplot as plt
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
        table_names = self.tables['name'].tolist()
        for table in table_names:
            self.graph.add_node(table, name=table)

        # Each arc is a foreign key constraint
        for index, fk in self.fks.iterrows():
            # The head of the arc is the foreign key's table
            from_table = fk['from_table']
            # The tail of the arc is the primary key's table
            to_table = fk['table']
            # The name of the arc is the name of the FK constraint
            from_col = fk['from']
            to_col = fk['to']
            # REMEMBER! Head is to and tail is from!
            self.graph.add_edge(to_table, from_table, from_col=from_col, to_col=to_col)

    def plot(self):
        """
        Draws the graph in Matplotlib.
        """
        nx.draw_shell(self.graph, arrowsize=16, node_color='#D3D3D3', node_size=1000, with_labels=True)
        plt.show()
        return

    def generate_user_data_report(self, user_id, user_table):
        """
        Finds all user data for a specified user, provided all foreign keys are correct.

        :param user_id: The desired user
        :param user_table: The table of users
        :return: JSON text of the user report
        """
        return

    def report_helper(self, key_id, from_table, to_table, from_col, to_col):
        """
        Recursive helper for :fun:generate_user_data_report.

        :param key_id: Primary key of the current table
        :param from_table: The table at the tail of the arc
        :param to_table: The table at the head of the arc
        :param from_col: The column including the key_id in from_table
        :param to_col: The column including the key_id in to_table
        :return: JSON object of user data
        """
        # report_q = "SELECT * FROM to-table WHERE from-table.from = to-table.to"
        # new_id = PK(results)
        #   BFS from new-from-table to each new-to-table:
        #   new-from-col = edge.from-col
        #   new-to-col = edge.to-col
        #   search-for-user-data(new-from-table, new-to-table, id, new-from-col, new-to-col)
        return
