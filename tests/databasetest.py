import unittest

from odlaw.connector import Connector
from odlaw.database import Database


class DatabaseTest(unittest.TestCase):

    def test_db_not_none(self):
        url = 'sqlite:///../sqlite/TPC-H-small.db'
        connector = Connector(url)
        database = Database(connector)
        self.assertIsNotNone(database)

    def test_tpc_h_search_small(self):
        url = 'sqlite:///../sqlite/TPC-H-small.db'
        connector = Connector(url)
        database = Database(connector)
        user_report = database.generate_user_data_report('CUSTOMER', 6)
        tables = user_report.tables
        # Number of tables affected
        self.assertEqual(len(tables), 3)
        # Number of records in user table
        self.assertEqual(len(tables.get('CUSTOMER')), 1)
        self.assertTrue(tables.get('ORDERS').empty)
        self.assertTrue(tables.get('LINEITEM').empty)

    def test_tpc_h_search(self):
        url = 'sqlite:///../sqlite/TPC-H-small.db'
        connector = Connector(url)
        database = Database(connector)
        user_report = database.generate_user_data_report('CUSTOMER', 4)
        tables = user_report.tables
        # Number of tables affected
        self.assertEqual(len(tables), 3)
        # Number of records in user table
        self.assertEqual(len(tables.get('CUSTOMER')), 1)
        self.assertEqual(len(tables.get('ORDERS')), 31)
        self.assertEqual(len(tables.get('LINEITEM')), 120)

    def test_connectedness(self):
        url = 'sqlite:///../sqlite/TPC-H-small.db'
        connector = Connector(url)
        database = Database(connector)
        # Number of records in user table
        self.assertTrue(database.is_connected())
        # Check components
        self.assertEqual(database.number_connected_components(), 1)


if __name__ == '__main__':
    unittest.main()
