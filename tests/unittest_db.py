from src.bt_utils.handle_sqlite import DatabaseHandler
import unittest
from pathlib import Path
import os
import shutil
import time
from sqlite3 import IntegrityError


class TestClass(unittest.TestCase):
    def testDB(self):
        if os.path.exists("content"):
            shutil.rmtree("content", ignore_errors=True)
        if not os.path.exists("content"):
            os.makedirs("content")
        else:
            try:
                os.remove("content/bundestag.db")
            except OSError:
                pass

        self.db = DatabaseHandler()
        self.roles = ["role1", "role2"]

        # creates basic table structures if not already present
        print("Create database and test if creation was successful")
        self.db.create_structure(self.roles)
        db_path = Path("content/bundestag.db")
        self.assertTrue(db_path.is_file())

        print("Check if database is empty")
        users = self.db.get_all_users()
        self.assertEqual(users, [])

        print("Add user to database and check if he exists.")
        self.db.add_user(123, self.roles)
        user = self.db.get_specific_user(123)
        self.assertEqual(user, (123, 0, 0))

        print("Add reaction to user and check if it exists.")
        self.db.add_reaction(123, "role1")
        user = self.db.get_specific_user(123)
        self.assertEqual(user, (123, 1, 0))

        print("Remove reaction and check if it does not exist anymore.")
        self.db.remove_reaction(123, "role1")
        user = self.db.get_specific_user(123)
        self.assertEqual(user, (123, 0, 0))

        print("Add another user and check if select all users works.")
        self.db.add_user(124, self.roles)
        users = self.db.get_all_users()
        self.assertEqual(users, [(123, 0, 0), (124, 0, 0)])

        print("Add another user with invalid id and check if it still get created.")
        with self.assertRaises(IntegrityError):
            self.db.add_user(124, self.roles)
        users = self.db.get_all_users()
        self.assertEqual(users, [(123, 0, 0), (124, 0, 0)])

        print("Add another column and check if it gets applied correctly")
        self.roles = ["role1", "role2", "role3"]
        self.db.update_columns(self.roles)

        users = self.db.get_all_users()
        self.assertEqual(users, [(123, 0, 0, 0), (124, 0, 0, 0)])

        print("Closing connection")
        del self.db


if __name__ == '__main__':
    unittest.main()
