"""
This script provide the interfaces for the Reception Pi local database
operation including insert, delete, query
"""
import MySQLdb

import pwd_encrypt as fp


class DatabaseUtils:
    """
    Local MariaDB database operation utils
    """
    HOST = "127.0.0.1"
    USER = "root"
    PASSWORD = "mugglermit"
    DATABASE = "Pi"
    PORT = 3306

    def __init__(self, connection=None):
        """
        Initialise the SQL connection using the in-code configuration
        :param connection:
        """
        if connection is None:
            connection = MySQLdb.connect(DatabaseUtils.HOST,
                                         DatabaseUtils.USER,
                                         DatabaseUtils.PASSWORD,
                                         DatabaseUtils.DATABASE,
                                         DatabaseUtils.PORT)

        self.connection = connection

    def close(self):
        """
        Close the sql connection
        """
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def create_user_table(self):
        """
        Create the User table if not exist
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE
            IF NOT EXISTS USER (
            username VARCHAR(25) NOT NULL,
            hash_password VARCHAR(20) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            CONSTRAINT PK_User PRIMARY KEY (username));
                    """)
        self.connection.commit()

    def insert_user(self, username, original_pass, first_name, last_name, email):
        """
        Insert a new user into the User table
        Should include username, password, first name, last name and email address
        :rtype: bool
        :param username: User's username
        :param original_pass: User's password (already encrypted)
        :param first_name: User's first name
        :param last_name: User's last name
        :param email: User's email address
        :return: True if insert successfully otherwise False
        """
        encrypted_pass = fp.encrypt(original_pass)
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO USER (username, hash_password,first_name,last_name,email) "
                "VALUES (%s, %s, %s, %s, %s)",
                (username, encrypted_pass, first_name, last_name, email))
        self.connection.commit()

        return cursor.rowcount == 1

    def check_is_exist(self, pre_ck_username):
        """
        Check if the username is already exist in the database
        :return True if the username is already used
        :rtype bool
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * "
                           "FROM USER WHERE username = %s", (pre_ck_username,))
        self.connection.commit()
        #
        return cursor.rowcount == 1

    def check_password(self, pre_ck_username, pre_ck_password):
        """
        Check if the income username's password match the database one
        :param pre_ck_username: income username
        :param pre_ck_password: income password inputted by external user
        :return: True if match else False
        :rtype bool
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT hash_password "
                           "FROM USER WHERE username = %s", (pre_ck_username,))
            row = cursor.fetchone()
        self.connection.commit()
        if row:
            return row[0] == fp.encrypt(pre_ck_password)
        return False

    def get_all_user(self):
        """
        Fetch all the user details
        :return: Str include all the user details
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM USER")
            return cursor.fetchall()

    def get_user_detail(self, username):
        """
        Wrap the specific user details that need to be sent to the Master Pi side
        :param username: the username used to match
        :return: User details in the dict format
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT username,first_name,last_name "
                           "FROM USER WHERE username = %s", (username,))
            row = cursor.fetchone()
        return {"Username": row[0], "FirstName": row[1], "LastName": row[2]}

    def del_user(self, username):
        """
        Delete the specific user
        :param username: refers to the username matched user
        """
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM USER WHERE username = %s", (username,))
        self.connection.commit()

    def init_insert(self):
        """
        For init the table data
        """
        try:
            self.create_user_table()
            self.insert_user("heiybb", "heiybb", "Bobin", "Yuan", "root@chr.moe")
            self.insert_user("hubert", "hubert", "Hubert", "Law", "hf.heiybb@gmail.com")
            self.insert_user("pied8", "rmit2019", "Emily", "Wilkinson", "terjesa@icloud.com")
            self.insert_user("gay8", "rmit2019", "Asher", "Emerson", "kawasaki@verizon.net")
            self.insert_user("suit8", "rmit2019", "Elaine", "Prentice", "yenya@hotmail.com")
            self.insert_user("map8", "rmit2019", "Akshay", "Odom", "tamas@outlook.com")
            self.insert_user("bleep8", "rmit2019", "Usama", "Daly", "martink@comcast.net")
            self.insert_user("step8", "rmit2019", "Tomas", "Powell", "dowdy@verizon.net")
            self.insert_user("hunky8", "rmit2019", "Kaci", "Norton", "mcraigw@yahoo.ca")
            self.insert_user("real8", "rmit2019", "Milly", "Heath", "rfisher@verizon.net")
            self.insert_user("mat8", "rmit2019", "Corben", "Cox", "tristan@aol.com")
            self.insert_user("essay8", "rmit2019", "Bret", "Tucker", "reeds@optonline.net")
            self.insert_user("meamy8", "rmit2019", "Aditi", "Burton", "north@outlook.com")
            self.insert_user("bagel8", "rmit2019", "Soren", "Estes", "padme@mac.com")
            self.insert_user("verde8", "rmit2019", "Silas", "Hutchinson", "overbom@live.com")
            self.insert_user("rice8", "rmit2019", "Humairaa", "Davila", "ardagna@hotmail.com")
            self.insert_user("trig8", "rmit2019", "Glenda", "Partridge", "kohlis@optonline.net")
        except MySQLdb.Error as sqlerror:
            print(sqlerror)


if __name__ == "__main__":
    DB_UTIL = DatabaseUtils()
    # DBUtil.init_insert()
