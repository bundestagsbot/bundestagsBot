from .console import Console
import sqlite3
SHL = Console(prefix="handleSQLITE")

BASE_PATH = "content/"
DB_PATH = "bundestag.db"


class DatabaseHandler:

    debug = False

    def __init__(self):
        self.con = sqlite3.connect(BASE_PATH + DB_PATH)

    def create_structure(self, roles):
        cursor = self.con.cursor()
        role_entries = ''
        for role in roles:
            role_entries += "\"" + role + '\" integer, '
        if len(role_entries) > 1:
            role_entries = role_entries[:-2]

        # create user table
        statement = "CREATE TABLE IF NOT EXISTS users(user_id integer PRIMARY KEY, " + role_entries + ")"
        cursor.execute(statement)
        self.con.commit()

    def update_columns(self, roles):
        cursor = self.con.cursor()
        statement = "PRAGMA table_info('users')"
        cursor.execute(statement)
        structure = cursor.fetchall()
        for role in roles:
            if role not in [col[1] for col in structure]:
                # add new role to table
                cursor.execute("ALTER TABLE users ADD \"" + role + "\" integer")
                if self.debug: SHL.output("Adding new role to users table " + role)
                self.con.commit()

    def add_user(self, uid, roles):
        cursor = self.con.cursor()
        roles_tuple = (0,) * len(roles)
        user = (uid,) + roles_tuple
        user_prep = "?, " * len(user)
        if len(user_prep) > 1:
            user_prep = user_prep[:-2]
        cursor.execute("INSERT INTO users VALUES (" + user_prep + ")", user)
        self.con.commit()

    def get_all_users(self):
        cursor = self.con.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        return rows

    def get_specific_user(self, uid):
        cursor = self.con.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ' + str(uid))
        user = cursor.fetchall()
        if len(user): return user[0]  # TODO: raise custom error and catch it in reactions.py line 21
        return ()

    def add_reaction(self, uid, role_reaction):
        cursor = self.con.cursor()

        # statement to increment reaction counter
        statement = "UPDATE users SET \"" + role_reaction + "\" = \"" + \
                    role_reaction + "\" + 1 WHERE user_id = " + str(uid)
        cursor.execute(statement)
        self.con.commit()
        if self.debug: SHL.output("added reaction to db")

    def remove_reaction(self, uid, role_reaction):
        cursor = self.con.cursor()

        # statement to increment reaction counter
        statement = "UPDATE users SET \"" + role_reaction + "\" = \"" + \
                    role_reaction + "\" - 1 WHERE user_id = " + str(uid)
        cursor.execute(statement)
        self.con.commit()
        if self.debug: SHL.output("removed reaction from db")

    def __del__(self):
        self.con.close()
