import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict


class LinksDB:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='12345', port=3306)
        self.db_cursor = self.cnx.cursor()

        self.db_name = 'sql_db'
        self.last_idx = 5000

        self.TABLES = OrderedDict()

        self.TABLES['links'] = (
            "CREATE TABLE `links` ("
            "  `name1` varchar(40) NOT NULL,"
            "  `name2` varchar(40) NOT NULL"
            ") ENGINE=InnoDB")

    def execute(self):
        query = """SELECT * FROM links """
        query1 = """SELECT * FROM links p1 JOIN links p2 ON p1.name1 = p2.name1 AND p1.name2 < p2.name2"""

        try:
            self.db_cursor.execute(query1)
            self.db_cursor.fetchall()
        except mysql.connector.Error as err:
            print(err.msg)

    def insert(self, name1, name2):
        try:
            statement = "INSERT INTO `sql_db`.`links`(`name1`, `name2`) VALUES ('"+name1+"','"+name2+"')"
            self.db_cursor.execute(statement)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)
            self.cnx.rollback()

    def create_table(self):
        for table_name in self.TABLES:
            try:
                print("Creating table {}: ".format(table_name))
                self.db_cursor.execute(self.TABLES[table_name])
                self.cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)

    def clear_table(self):
        for table_name in self.TABLES:
            try:
                self.db_cursor.execute("DELETE FROM "+table_name)
                self.cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("error in clearing table")
                else:
                    print(err.msg)

    def create_database(self):
        try:
            print("Creating database: {}".format(self.db_name))
            self.db_cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        self.cnx.database = self.db_name

    def connect_database(self):
        try:
            self.cnx.database = self.db_name
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
            else:
                print(err)
                exit(1)

    def drop_database(self):
        try:
            print("Dropping database: {}".format(self.db_name))
            self.db_cursor.execute("DROP DATABASE {}".format(self.db_name))
        except mysql.connector.Error as err:
            print("Failed dropping database: {}".format(err))
            exit(1)

        self.db_cursor.close()
        self.cnx.close()
