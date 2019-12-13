import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import os
import glob

from zipfile import ZipFile
from odlaw.report import Report


class Database:
    """
    A representation of a database as a graph.
    """

    def __init__(self, connector):

        # Initialize member variables
        self.connector = connector

        # Query for table names
        self.tables = self.connector.query_tables()

        # Query for primary keys
        self.pks = self.connector.query_pks()

        # Query for foreign keys
        self.fks = self.connector.query_fks()

        # The database is represented by a graph
        self.graph = nx.MultiDiGraph()

        # Each node is a table in the database
        table_names = self.tables['name'].tolist()
        for table in table_names:
            # Fetch the primary key of the table
            pk = self.pks.get(table)

            # Add the node with name as table name
            self.graph.add_node(table, name=table, pk=pk)

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
        :return: A Report containing a dictionary of pandas DFs for all user report sub-tables
        """
        # Create a report to keep track of everything
        user_report = Report(user_id)

        # Fetch the PK
        primary_key = self.pks.get(user_table)

        # Add entry to the Report
        data = self.connector.query_for_report(user_table, primary_key, str(user_id))

        # Write data to dict
        user_report.add_table_entries(user_table, data)

        # Convert user_id to a list
        id_list = [user_id]

        # Start from user table and search to all dependent data
        self.visit(user_table, id_list, user_report)

        # Return the built-up Report object
        return user_report

    def visit(self, node, values, user_report):
        """
        A recursive search through the graph representation of the database.
        Used to generate a Report.

        :param node: The name of the node to be visited
        :param values: A list of values (FK) linking from the previous table
        :param user_report: A Report object to build up.
        :return: Boolean of whether success or failure
        """
        # Get all edges from root node
        neighbors = self.graph.neighbors(node)
        for neighbor in neighbors:
            # Get names of edges: columns to check
            edge_data = self.graph.get_edge_data(node, neighbor)
            # NetworkX wraps the attributes dict in a dict
            edge_data = edge_data[0]
            from_col = edge_data['from_col']

            # Get neighbors of root_nodes
            in_values = self.list_to_string(values)
            if in_values == "":
                data = pd.DataFrame()
            else:
                data = self.connector.query_for_report(neighbor, from_col, in_values)

            # Write data to dict
            user_report.add_table_entries(neighbor, data)

            # Fetch primary key and get values for next call
            primary_key = self.pks.get(neighbor)

            try:
                # If there's more, than recurse
                new_values = user_report.tables.get(neighbor)[primary_key].unique().tolist()
                self.visit(neighbor, new_values, user_report)
            except KeyError:
                if self.connector.verbose:
                    print("No entries in %s. Terminating search from this node." % node)

        # Return success
        return True

    def generate_csv_user_data_report(self, user_table, user_id, location, prefix='report', sep=','):
        """
        Calls generate_user_data_report and writes the resulting tables to a CSV file.

        :param prefix: Prefix of the report name
        :param location: The folder to output the saved contents
        :param user_id: The desired user's unique ID
        :param user_table: The table of users
        :param sep: The delimiter to be used in the output CSV file
        :return: True if all dataframes were saved successfully, false otherwise
        """
        saves = []
        report = self.generate_user_data_report(user_table, user_id)
        tables = report.tables
        for table_name, data_frame in tables.items():
            output_url = "%s/%s_%s.csv" % (location, prefix, table_name)
            did_save = data_frame.to_csv(output_url, sep=sep)
            saves.append(did_save)
            # Write out dataframe to a csv file

        # Zip up data-frames to a single zip archive
        zip_url = '%s/%s_tables.zip' % (location, prefix)
        with ZipFile(zip_url, 'w') as zf:
            for csv in glob.glob('%s/*.csv' % location):
                zf.write(csv)
                os.remove(csv)  # Zipped it, so remove it

        # We were successful if all saves went through
        if all(save is not None for save in saves):
            return True
        # We were unsuccessful if there was a failure
        else:
            return False

    def block_primary_keys(self, report):
        """
        Censors a report to exclude any primary keys

        :param report: A Report object
        :return: A 'censored' report object
        """
        # Iterate over PKs (NOT TABLES) (DBA may not have specified pk)
        for table in self.pks:
            # Access the report table
            try:
                # Go to the table in the report and drop the column
                old_tables = report.tables.get(table)
                censored = old_tables.drop(columns=[self.pks[table]])
                report.tables[table] = censored
            # Empty DF
            except AttributeError:
                if self.connector.verbose:
                    print("Empty dataframe")

        # Done, so return amended report
        return report

    def remove_user(self, user_table, user_id):
        """
        Removes a user (and all of their dependent data) from the database.

        :param user_table: The name of the table where user data is stored.
        :param user_id: The unique identifier of the user to be deleted.
        :return:
        """
        # Generate a report to know where to look
        report = self.generate_user_data_report(user_table, user_id)
        tables = report.tables
        pks = self.pks
        user_component_names = list(tables.keys())
        user_component = self.graph.subgraph(user_component_names)
        top_sort = nx.topological_sort(user_component)
        rev_top_sort = list(reversed(list(top_sort)))
        # Remove data from every affected table
        for node in rev_top_sort:
            table = tables.get(node)
            pk = pks.get(node)
            try:
                values = table[pk].unique().tolist()
                in_values = self.list_to_string(values)
                if not table.empty:
                    self.connector.query_for_deletion(node, pk, in_values)
            except KeyError:
                if self.connector.verbose:
                    print("No entries to delete from %s", table)
        return

    def is_connected(self):
        """
        Checks if the database graph is connected.

        :return: True if the graph is connected, False otherwise
        """
        return nx.is_connected(nx.to_undirected(self.graph))

    def connected_components(self):
        """
        Finds the connected components of the database graph.

        :return: The connected components of the database graph
        """
        return nx.connected_components(nx.to_undirected(self.graph))

    def number_connected_components(self):
        """
        Finds the number of connected components of the database graph.

        :return: The number connected components of the database graph
        """
        return nx.number_connected_components(nx.to_undirected(self.graph))

    @staticmethod
    def list_to_string(list_of_stuff):
        return str(list_of_stuff).strip('[]')

    @staticmethod
    def block(report, blocks):
        """
        Creates a 'censored' version of the report.

        :param report: A Report object to sensor
        :param blocks: A list of <TABLE>.<COLUMN> entries to be removed from the report
        :return: A 'censored' Report object
        """
        # Go through every constraint
        for block in blocks:
            # Find the table and column
            block_split = block.split('.')  # Split with '.'
            table = block_split[0]
            column = block_split[1]
            # Go to the table in the report and drop the column
            old_tables = report.tables.get(table)
            censored = old_tables.drop(columns=[column])
            report.tables[table] = censored

        # Done, so return the censored report
        return report
