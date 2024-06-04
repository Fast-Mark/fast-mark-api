import logging
import sqlite3

from src.modules import UserInDB


class UsersDB():
    def __init__(self) -> None:
        self.db = sqlite3.connect('FastMark.sqlite')
        self.sql = self.db.cursor()

        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT,
                    hashedPassword TEXT,
                    email TEXT,
                    disabled BOOLEAN
        )""")
        self.db.commit()

    def create_user(self, user_name, user_password, user_emeil):
        if (user_name == None) or (user_password == None):
            return False

        self.sql.execute(f"SELECT name FROM users WHERE name = '{user_name}'")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO users VALUES (?,?,?,?)", (user_name, user_password, user_emeil, False))
            self.db.commit()
            # добавлен новый пользователь
        else:
            return Exception("user with self name already exists")

    def get_user(self, user_name):
        if (user_name == None):
            return None

        self.sql.execute("SELECT * FROM users WHERE name = ?", (user_name,))
        db_user = self.sql.fetchone()
        if db_user is None:
            return None

        user = UserInDB.from_db_row(db_user)
        return user

    def get_all_users(self):
        list_users = list()
        for value in self.sql.execute("SELECT * FROM users"):
            list_users.append(value)

        return list_users

    def delete(self):
        self.sql.execute("DROP TABLE IF EXISTS users")

# all_users = UsersDB()

# print(all_users.create_user('Amir', 'ggggggs', 'amralt@gmail.com'))
# print(all_users.get_user("Amir"))

# print(all_users.getAllUsers())
# print(all_users.get_user_password('amir'))
