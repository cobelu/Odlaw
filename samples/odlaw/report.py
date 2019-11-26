class Report:
    """
    A representation of a Report for a user.
    """

    def __init__(self, user_id):
        self.tables = {}

    def add_table_entries(self, table, table_data):
        if table in self.tables:
            self.tables[table].concat(table_data)
        else:
            self.tables[table] = table_data
        return True

    def print_report(self):
        for table in self.tables:
            print(self.tables.get(table))
            print()
