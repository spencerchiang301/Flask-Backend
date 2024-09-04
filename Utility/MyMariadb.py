import mariadb
import sys


class MyMariadb:
    def __init__(self, user, password, host, port, db):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.conn = None
        self.cursor = None

    def changeDB(self, db):
        self.db = db

    def initConn(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db)
            self.cursor = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def query(self, query):
        try:
            self.cursor.execute(query)
        except mariadb.Error as e:
            print(f'Error: {e}')

    def InsertUpdateAndDelete(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")

    def close(self):
        self.conn.close()
