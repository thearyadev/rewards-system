import sqlite3
import datetime
import pathlib
import typing


class Database:
    """
    Manages the databases (income and expenses) used within the program.
    """

    def __init__(self, name: str, path: typing.Union[str, pathlib.Path]):
        self.connection = sqlite3.connect(path, check_same_thread=False)  # open the db with path passed in
        self.name = name  # this is also the name of the table of the sqlite3 database
        self.cursor = self.connection.cursor()  # init cursor
        self.cursor.execute(  # create table if it does not exist
            f"CREATE TABLE IF NOT EXISTS {self.name} (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INTEGER, item TEXT, price INTEGER)")

    def add(self, **item):
        """
        Adds an item to the database
        :param item: This is the item object passed in as an unpacked dictionary
        :return:
        """
        self.cursor.execute(f"INSERT INTO {self.name} (timestamp, item, price) values (?, ?, ?)",
                            (datetime.datetime.now().timestamp(), item['name'], item['price'],))  # insert
        self.connection.commit()  # commit

    def query_all(self):
        """
        Gets all entries from the database
        :return:
        """
        return self.cursor.execute(f"SELECT * FROM {self.name}").fetchall()[::-1]  # query all and reverse the list

    def sum(self) -> typing.Union[int, float]:
        """
        get the sum of all entries in the database
        :return:
        """
        data = self.cursor.execute(f"SELECT * FROM {self.name}").fetchall()  # fetch all entries
        if len(data) == 0 or data is None:  # check if the data exists or has any entries.
            return 0
        return sum([i[3] for i in data])  # i[3] is the amount, sum of the list of the amounts.
