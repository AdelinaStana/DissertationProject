import mysql.connector
from mysql.connector import errorcode
from collections import OrderedDict
import csv


class LinksDB:
    def __init__(self, working_dir):
        self.cnx = mysql.connector.connect(user='root', password='12345', port=3306)
        self.db_cursor = self.cnx.cursor()
        self.working_dir = working_dir

        self.db_name = 'sql_db'
        self.last_idx = 1
        self.insert_count = 0
        self.chunk_nr = 0
        self.current_csv_path = self.working_dir+"/DB"+str(self.last_idx)+".csv"
        self.writer = csv.writer(open(self.current_csv_path, 'w+'))

        self.TABLES = OrderedDict()

        for i in range(1, 34):
            self.TABLES['links'+str(i)] = (
                "CREATE TABLE `links"+str(i)+"` ("
                "  `name1` VARCHAR(500) NOT NULL,"
                "  `name2` VARCHAR(500) NOT NULL"
                ") ENGINE=InnoDB")

    def increment_indexes(self):
        self.last_idx += 1
        self.current_csv_path = self.working_dir + "/DB" + str(self.last_idx) + ".csv"
        self.writer = csv.writer(open(self.current_csv_path, 'w+'))
        self.insert_count = 0

    def load_csv(self):
        del self.writer

        data = '''LOAD DATA LOCAL INFILE \'''' + str(self.current_csv_path) + '''\' INTO TABLE links''' + str(
            self.last_idx) + ''' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' '''
        try:
            self.db_cursor.execute(data)
            self.cnx.commit()
        except:
            print("Could not insert csv to database!")

        if self.insert_count > 15000:
            self.insert_count = 0
            self.chunk_nr += 1
            self.current_csv_path = self.working_dir + "/DB" + str(self.last_idx)+"_chunk"+str(self.chunk_nr) + ".csv"
            self.writer = csv.writer(open(self.current_csv_path, 'w+'))

    def count(self):
        self.load_csv()
        query = "SELECT COUNT(DISTINCT name1,name2) FROM links"+str(self.last_idx)
        number_of_rows = -1
        try:
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchone()
            if result:
                number_of_rows = result[0]
        except mysql.connector.Error as err:
            print(err.msg)

        self.increment_indexes()
        return number_of_rows

    def insert(self, name1, name2):
        self.insert_count += 1
        self.writer.writerow([name1, name2])
        if self.insert_count > 15000:
            self.load_csv()
    '''
    def insert(self, name1, name2):
        try:
            statement = "INSERT INTO `sql_db`.`links"+str(self.last_idx)+"`(`name1`, `name2`) VALUES ('"+name1+"','"+name2+"')"
            self.db_cursor.execute(statement)
            self.insert_count += 1
            if self.insert_count == 5000:
                self.cnx.commit()
                self.insert_count = 0
        except mysql.connector.Error as err:
            return'''

    def create_tables(self):
        print("Creating tables...")
        try:
            for table_name in self.TABLES:
                self.db_cursor.execute(self.TABLES[table_name])
                self.db_cursor.execute("CREATE UNIQUE INDEX indexname ON " + table_name+ "(name1,name2)")
            self.cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("cannot create tables")
            else:
                print(err.msg)

    def drop_tables(self):
        print("Drop tables...")
        for table_name in self.TABLES:
            try:
                self.db_cursor.execute("DROP TABLE " + table_name)
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
