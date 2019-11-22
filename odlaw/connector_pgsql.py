from odlaw.connector import Connector

import pandas as pd


class ConnectorPostgreSQL(Connector):

    def __init__(self, database):
        super().__init__(self)
        self.database = database

    def query_tables_pgsql(self):
        """
        Asks a PostgreSQL DB for its tables.

        :return: A pandas DF of tables in the PGSQL DB
        """
        # http://www.postgresqltutorial.com/postgresql-show-tables/
        # TODO: Simplify query
        tables_q = "SELECT *"
        tables_q += "FROM pg_catalog.pg_tables"
        tables_q += "WHERE schemaname != \'pg_catalog\'"
        tables_q += "AND schemaname != \'information_schema\';"
        tables = self.query(tables_q)
        # Return the column of table names
        tables = tables['tablename']
        return tables


    def add_fk_constraint_pgsql(self, from_table, to_table, from_col, to_col, name, cascade=True):
        """
        Adds a foreign key constraint to the database.

        :param from_table: The table containing the primary key
        :param from_col: The primary key column in the from table
        :param to_table: The table containing the foreign key
        :param to_col: The foreign key column in the to table
        :param name: The name of the foreign key constraint
        :param cascade: If should add 'on delete cascade'
        :return: Boolean representing success
        """
        # TODO: ASK "ARE YOU SURE?" FIRST (OUTSIDE OF THIS FUNCTION WHERE THE FUNCTION IS CALLED)!!!

        # Build a query
        query = "ALTER TABLE %s" % to_table
        query += "ADD CONSTRAINT %s" % name
        query += "FOREIGN KEY (%s)" % to_col
        query += "REFERENCES %s(%s)" % (from_table, from_col)
        if cascade:
            query += "ON DELETE CASCADE"
        query += ";"

        # Add constraint
        self.query(query)
        return True
