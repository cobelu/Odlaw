class Report:
    """
    A representation of a Report for a user.
    """

    def __init__(self, user_id):
        self.tables = {}

    def add_table_entries(self, table, table_data):
        """
        Adds a table entry to the tables dictionary.

        :param table: The name of the table
        :param table_data: The contents of the table
        """
        if table in self.tables:
            self.tables[table].concat(table_data)
        else:
            self.tables[table] = table_data
        return True

    def print_report(self):
        """
        Prints the report object to the console.
        """
        for table in self.tables:
            print(self.tables.get(table))
            print()
