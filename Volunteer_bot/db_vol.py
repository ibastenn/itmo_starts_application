import sqlite3
import time

from db_event import DBE

dbe = DBE('users.db')


class DBV:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def select_user_name(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if res is not None and res[0] is not None:
                return res[0]
            else:
                return ""

    def select_user_age(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_age FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if res is not None and res[0] is not None:
                return res[0]
            else:
                return ""

    def select_user_mail(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_mail FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if res is not None and res[0] is not None:
                return res[0]
            else:
                return ""

    def select_user_vk(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_vk FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if res is not None and res[0] is not None:
                return res[0]
            else:
                return ""

    def select_user_tg(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_tg FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if res is not None and res[0] is not None:
                return res[0]
            else:
                return ""

    def edit_user_name(self, user_id, user_name):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (user_name, user_id,))

    def edit_user_age(self, user_id, user_age):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_age = ? WHERE user_id = ?", (user_age, user_id,))

    def edit_user_email(self, user_id, user_mail):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_mail = ? WHERE user_id = ?", (user_mail, user_id,))

    def edit_user_vk(self, user_id, user_vk):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_vk = ? WHERE user_id = ?", (user_vk, user_id,))

    def edit_user_tg(self, user_id, user_tg):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_tg = ? WHERE user_id = ?", (user_tg, user_id,))

    def get_edit_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if result is not None:
                signup = result[0]
            else:
                signup = ""
            return signup

    def set_edit_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id,))

    def active_events(self, user_id):
        with self.connection:
            a = []
            result = self.cursor.execute("SELECT short_name FROM volunteers WHERE user_id = ?", (user_id,)).fetchall()
            nowatime = round(time.time() * 1000)
            for row in result:
                if row is not None and (nowatime <= dbe.get_end_times(row[0])):
                    a += [row]
            return a
