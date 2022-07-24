import sqlite3
import time


class DB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # добавление
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    # существует ли уже        
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    # указываем ФИО
    def set_user_name(self, user_id, user_name):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (user_name, user_id,))

    # указываем возраст
    def set_user_age(self, user_id, user_age):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_age = ? WHERE user_id = ?", (user_age, user_id,))

    # указываем почту
    def set_user_email(self, user_id, user_mail):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_mail = ? WHERE user_id = ?", (user_mail, user_id,))

    # указываем vk
    def set_user_vk(self, user_id, user_vk):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_vk = ? WHERE user_id = ?", (user_vk, user_id,))

    # указываем telegram
    def set_user_tg(self, user_id, user_tg):
        with self.connection:
            return self.cursor.execute("UPDATE users SET user_tg = ? WHERE user_id = ?", (user_tg, user_id,))

    # статус регистрации
    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if result is not None:
                signup = result[0]
            else:
                signup = ""
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id,))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))

    def get_mess_for_vol(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM users").fetchall()

    def milli_time(self):
        return round(time.time() * 1000)
