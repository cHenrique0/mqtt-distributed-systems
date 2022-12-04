import sqlite3
from datetime import datetime


def connect(file: str) -> sqlite3.Connection:
    """
    Connect to a SQLite database file.

    Returns:
        sqlite3.Connection: the instance of database connection
    """

    try:
        database = sqlite3.connect(file)
        print(f"Database successfully connected to <{file}>")
    except:
        print("Database not connected.")

    return database


# def create_table(database: sqlite3.Connection, table: str, columns: list) -> None:
def create_table(database: sqlite3.Connection) -> None:
    """
    Create a table in the database.

    Args:
        database (sqlite3.Connection): the database connection
    """
    with database:
        cursor = database.cursor()
        # cursor.execute(
        #     f"CREATE TABLE IF NOT EXISTS {table.capitalize()}({columns[0]} VARCHAR(10) PRIMARY KEY, {columns[1]} TEXT, {columns[2]} TEXT, {columns[3]} FLOAT, {columns[4]} DATETIME)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Sensors(id VARCHAR(10) PRIMARY KEY, area TEXT, sensor_type TEXT, value FLOAT, created_at DATETIME)")


def drop_table(database: sqlite3.Connection, table: str) -> None:
    """
    Drop a table in the database.

    Args:
        database (sqlite3.Connection): the database connection
        table (str): the name of the table to drop
    """

    with database:
        cursor = database.cursor()
        cursor.execute(f"DROP TABLE {table.capitalize()}")


def insert(database: sqlite3.Connection, table: str, values: list) -> None:
    """
    Insert data into a table.

    Args:
        database (sqlite3.Connection): the database connection
        table (str): the table name to insert data
        values (list): a list of values to insert in the table
    """

    values.append(datetime.now())

    query = f"INSERT INTO {table.capitalize()} VALUES(?, ?, ?, ?, ?)"

    with database:
        cursor = database.cursor()
        cursor.execute(query, values)


def select(database: sqlite3.Connection, table: str) -> list:
    """
    Select data from a table.

    Args:
        database (sqlite3.Connection): the database connection
        table (str): the name of the table to select data

    Returns:
        list: a list of tuples with the data
    """

    datas = []

    with database:
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM {table.capitalize()}")
        rows = cursor.fetchall()

        for data in rows:
            datas.append(data)

    return datas


def update(database: sqlite3.Connection, table: str, new_values: list) -> None:
    """
    Update data in a table.

    Args:
        database (sqlite3.Connection): the database connection
        table (str): the name of the table to update data
        new_values (list): a list of new values to update in the table
    """

    query = f"UPDATE {table.capitalize()} SET value = ? WHERE id = ?"

    with database:
        cursor = database.cursor()
        cursor.execute(query, new_values)
