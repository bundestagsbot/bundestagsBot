from .console import Console
import sqlite3

SHL = Console(prefix="handleSQLITE")

BASE_PATH = "content/"
DB_PATH = "bundestag.db"


class DatabaseHandler:

    def __init__(self):
        self.con = sqlite3.connect(BASE_PATH + DB_PATH)

    def create_structure(self, roles):
        cursor = self.con.cursor()

        role_entries = ''
        for role in roles:
            role_entries += role + ' integer, '
        if len(role_entries) > 1:
            role_entries = role_entries[:-2]

        # create user table
        statement = "CREATE TABLE IF NOT EXISTS users(user_id integer PRIMARY KEY, " + role_entries + ")"
        cursor.execute(statement)
        self.con.commit()

    def add_user(self, uid, name):
        cursor = self.con.cursor()
        user = (uid, name)
        # cursor.execute("INSERT INTO users VALUES (?, ?, 0)", user)
        # self.con.commit()

    def update_user_count(self, user_id, count):
        cursor = self.con.cursor()
        # cursor.execute("UPDATE users SET count = " + str(count) + " where id = " + str(user_id))
        # self.con.commit()

    def get_all_users(self):
        cursor = self.con.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        print(rows)
        return rows

    def add_reaction(self, reaction_recipiant, role_reaction):
        SHL.output("added reaction to db")

    def remove_reaction(self):
        SHL.output("removed reaction from db")

    def __del__(self):
        self.con.close()
