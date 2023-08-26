import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def select_number(self):
        with self.connection:
            result = self.cursor.execute("SELECT number FROM nums WHERE id=1", ())
            return result.fetchone()[0]

    def numberplusone(self):
        with self.connection:
            self.cursor.execute("UPDATE nums SET number = number + 1 WHERE id=1", ())
