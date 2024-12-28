"""
=============================================================================

  Licensed Materials, Property of Ralph Vogl, Munich

  Project : backtraderfunctions

  Copyright (c) by Ralph Vogl

  All rights reserved.

  Description:

  a simple database abstraction layer for SQLite, MySQL, and PostgreSQL

=============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import sqlite3
import psycopg2
import mysql.connector
from urllib.parse import urlparse
from sqlalchemy import create_engine

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
class DataBaseHandler:
    """
    Abstract base class for all databases.

    Methods
    -------
    connect(connection_string: str):
        Establishes a connection to the database.

    close():
        Closes the connection to the database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.
    """

    def connect(self, connection_string: str):
        """Establishes a connection to the database."""
        raise NotImplementedError

    def close(self):
        """Closes the connection to the database."""
        raise NotImplementedError

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        raise NotImplementedError

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        raise NotImplementedError

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        raise NotImplementedError

    def get_connection(self):
        """Returns the connection object for use with pandas."""
        raise NotImplementedError

    def begin_transaction(self):
        """Begins a transaction."""
        raise NotImplementedError

    def commit(self):
        """Commits the current transaction."""
        raise NotImplementedError

    def rollback(self):
        """Rolls back the current transaction."""
        raise NotImplementedError


class SQLiteDataBaseHandler(DataBaseHandler):
    """
    Implementation of the Database abstraction for SQLite.

    Methods
    -------
    connect(connection_string: str):
        Establishes a connection to the SQLite database.

    close():
        Closes the connection to the SQLite database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.lastQueryString = None

    def connect(self, connection_string: str):
        """Establishes a connection to the SQLite database."""
        self.connection = sqlite3.connect(connection_string)
        self.cursor = self.connection.cursor()

    def close(self):
        """Closes the connection to the SQLite database."""
        if self.cursor:
            self.cursor.close()  # Cursor schließen
        if self.connection:
            self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        self.cursor.execute(query, parameters)
        self.connection.commit()

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        if new_query or (query != self.lastQueryString):
            self.cursor.execute(query, parameters)
            self.lastQueryString = query
        columns = [desc[0] for desc in self.cursor.description]
        result = self.cursor.fetchone()
        return dict(zip(columns, result)) if result else None

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        self.cursor.execute(query, parameters)
        columns = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]

    def get_connection(self):
        """Returns the connection object for use with pandas."""
        return self.connection

    def begin_transaction(self):
        """Begins a transaction."""
        self.connection.execute("BEGIN")

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()


class MySQLDataBaseHandler(DataBaseHandler):
    """
    Implementation of the Database abstraction for MySQL.

    Methods
    -------
    connect(connection_string: dict):
        Establishes a connection to the MySQL database.

    close():
        Closes the connection to the MySQL database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.lastQueryString = None

    def connect(self, connection_string: str):
        """Establishes a connection to the MySQL database using a connection URL."""

        # Parse die URL mit urlparse
        result = urlparse(connection_string)

        # Erstelle ein Dictionary aus den Verbindungsparametern
        connection_info = {
            "user": result.username,
            "password": result.password,
            "host": result.hostname,
            "port": result.port,
            "database": result.path[1:],  # remove the leading '/'
        }

        # Stelle die Verbindung her
        self.connection = mysql.connector.connect(**connection_info)

    def close(self):
        """Closes the connection to the MySQL database."""
        if self.cursor:
            self.cursor.close()  # Cursor schließen
        if self.connection:
            self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        self.cursor.execute(query, parameters)
        self.connection.commit()

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        if new_query or (query != self.last_query_string):
            self.cursor.execute(query, parameters)
            self.last_query_string = query
        return self.cursor.fetchone()

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def get_connection(self):
        """Returns the connection object for use with pandas."""
        return self.connection

    def begin_transaction(self):
        """Begins a transaction."""
        self.connection.start_transaction()

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()


class PostgreSQLDataBaseHandler(DataBaseHandler):
    """
    Implementation of the Database abstraction for PostgreSQL.

    Methods
    -------
    connect(connection_string: str):
        Establishes a connection to the PostgreSQL database.

    close():
        Closes the connection to the PostgreSQL database.

    execute(query: str, parameters: tuple = ()):
        Executes a non-returning query (e.g., INSERT, UPDATE, DELETE).

    fetch_one(query: str, parameters: tuple = ()) -> dict:
        Retrieves a single record.

    fetch_all(query: str, parameters: tuple = ()) -> list:
        Retrieves all records.

    get_connection():
        Returns the connection object for use with pandas.

    begin_transaction():
        Begins a transaction.

    commit():
        Commits the current transaction.

    rollback():
        Rolls back the current transaction.
    """

    def __init__(self):
        self.connection = None
        self.engine = None  # Add an engine variable
        self.cursor = None
        self.last_query_string = None

    def connect(self, connection_string: str):
        """Establishes a connection to the PostgreSQL database using a connection URL."""
        result = urlparse(connection_string)

        # Get the protocol/scheme
        protocol = result.scheme  # This will typically be 'postgresql'

        connection_info = {
            "user": result.username,
            "password": result.password,
            "host": result.hostname,
            "port": result.port,
            "database": result.path[1:],  # remove the leading '/'
        }

        # You can check if the protocol is 'postgresql' before proceeding
        if protocol != "postgresql":
            raise ValueError("Invalid protocol: {}".format(protocol))

        self.connection = psycopg2.connect(**connection_info)
        self.engine = create_engine(connection_string)
        self.cursor = self.connection.cursor()

    def close(self):
        """Closes the connection to the PostgreSQL database."""
        if self.cursor:
            self.cursor.close()  # Cursor schließen
        if self.connection:
            self.connection.close()

    def execute(self, query: str, parameters: tuple = ()):
        """Executes a non-returning query (e.g., INSERT, UPDATE, DELETE)."""
        self.cursor.execute(query, parameters)
        self.connection.commit()

    def fetch_one(self, query: str, new_query: bool = False, parameters: tuple = ()) -> dict:
        """Retrieves a single record."""
        if new_query or (query != self.last_query_string):
            self.cursor.execute(query, parameters)
            self.last_query_string = query
        columns = [desc[0] for desc in self.cursor.description]
        result = self.cursor.fetchone()
        return dict(zip(columns, result)) if result else None

    def fetch_all(self, query: str, parameters: tuple = ()) -> list:
        """Retrieves all records."""
        self.cursor.execute(query, parameters)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_connection(self):
        """Returns the SQLAlchemy engine for use with pandas."""
        return self.engine

    def begin_transaction(self):
        """Begins a transaction."""
        self.connection.autocommit = False

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()
