import networkx


class Database:
    """
    A representation of a database as a graph.
    """

    def __init__(self, connector):

        # Initialize member variables
        self.connector = connector

        # TODO: initialize a graph object from networkx from the given connector object

    def plot(self):
        # TODO: Export the graph as a matplotlib plot
        print("I'm drawing myself in networkx!")
