import matplotlib.pyplot as plt
import networkx as nx

from odlaw.report import Report


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

    def generate_user_data_report(self, user_table, user_id):
        """
        Finds all user data for a specified user, provided all foreign keys are correct.

        :param user_table: The table of users
        :param user_id: The desired user
        :return: A dictionary of pandas DFs for all user report sub-tables
        """
        # Create a report to keep track of everything
        user_report = Report(user_id)
        # Start from user table and search to all dependent data
        self.visit(user_table, user_id, user_report)
        return user_report

    def visit(self, node, values, user_report):
        # TODO: Fix visit algorithm
        # TODO: Fix base case
        # Get all edges from root node
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            # Get names of edges: columns to check
            edge_data = self.graph.get_edge_data(node, neighbor)
            # NetworkX wraps the attributes dict in a dict
            edge_data = edge_data[0]
            print(edge_data)
            from_col = edge_data['from_col']
            to_col = edge_data['to_col']

            print("(from_col, to_col)=(%s, %s)" % (from_col, to_col))

            # Get neighbors of root_nodes
            in_values = self.list_to_string(values)
            print(in_values)
            data = self.connector.query_for_data(node, to_col, in_values)

            # Write data to dict
            user_report.add_table_entries(neighbor, data)

            # Extract unique ID vals from data and send to new_values
            new_values = data[to_col].unique().tolist()
            self.visit(neighbor, new_values, user_report)
        return True

    def generate_csv_user_data_report(self, user_id, user_table, location=None, prefix='report', sep=','):
        """
        Calls generate_user_data_report and writes the resulting tables to a CSV file.

        :param prefix: Prefix of the report name
        :param location: The folder to output the saved contents
        :param user_id: The desired user's unique ID
        :param user_table: The table of users
        :param sep: The delimiter to be used in the output CSV file
        :return: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
        """
        saves = []
        report = self.generate_user_data_report(user_id, user_table)
        tables = report.tables
        for table in tables:
            # Fetch name of table
            table_name = 'TABLE_NAME'
            output_url = "%s/%s_%s.csv" % (location, prefix, table_name)
            did_save = table.to_csv(output_url, sep=sep)
            saves.append(did_save)
        # TODO: Zip up data-frames to a single zip archive?
        # We were successful if all saves went through
        if all(save is not None for save in saves):
            return True
        # We were unsuccessful if there was a failure
        else:
            return False

    @staticmethod
    def list_to_string(list_of_stuff):
        return str(list_of_stuff).strip('[]')
