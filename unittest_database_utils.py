"""
Unit test for the database utils module
"""
import unittest

from database_utils import DatabaseUtils


class TestDatabaseUtils(unittest.TestCase):
    """
    Test the database utils function integration
    """

    def setUp(self):
        """
        Call the DatabaseUtils module
        """
        self.dtu = DatabaseUtils()
        self.db_connection = self.dtu.connection

        # drop the table if it already exists
        # for the clean test environment
        with self.db_connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS USER")
            self.db_connection.commit()

        self.dtu.create_user_table()
        self.dtu.init_test_users()

    def tearDown(self):
        """
        Close the database connection
        Clean the test environment
        :return:
        """
        try:
            self.db_connection.close()
        except:
            pass
        finally:
            self.db_connection = None

    def count_user_amount(self):
        """
        Wrap the count user method using the
        module build-in method
        """
        return len(self.dtu.get_all_user())

    def test_insert_user(self):
        """
        Test if the insertion match the validation
        :return:
        """
        count = self.count_user_amount()

        self.assertFalse(self.dtu.insert_user("heiybb", '2019', 'rmit', 'melbourne', 'root@rmit.cc'))
        # 'heiybb' already exist such that count user should equals to count before
        self.assertTrue(count == self.count_user_amount())

        self.assertTrue(self.dtu.insert_user("Jerry", '2019', 'rmit', 'melbourne', 'root@rmit.cc'))
        self.assertTrue(count + 1 == self.count_user_amount())

        self.assertTrue(self.dtu.insert_user("Tom", '2019', 'rmit', 'melbourne', 'root@rmit.cc'))
        self.assertTrue(count + 2 == self.count_user_amount())

    def test_delete_user(self):
        """
        Test if the deletion result match the after count
        :return:
        """
        # delete an existed user
        count = self.count_user_amount()
        self.assertTrue(self.dtu.check_is_exist('mat8'))
        self.dtu.del_user('mat8')
        self.assertFalse(self.dtu.check_is_exist('mat8'))
        self.assertTrue(count - 1 == self.count_user_amount())

        # delete an non-existed user
        count = self.count_user_amount()
        self.assertFalse(self.dtu.check_is_exist('no-existed'))
        self.dtu.del_user('no-existed')
        self.assertFalse(self.dtu.check_is_exist('no-existed'))
        self.assertTrue(count == self.count_user_amount())


if __name__ == "__main__":
    unittest.main()
