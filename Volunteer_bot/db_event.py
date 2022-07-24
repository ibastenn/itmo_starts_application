import sqlite3

class DBE:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_supply(self, user_id, short_name, user_name, user_age, user_mail, user_vk, user_tg, time_press):
        with self.connection:
            return self.cursor.execute("INSERT INTO volunteers (user_id, short_name, user_name, user_age, user_mail, user_vk, user_tg, time_press) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                       (user_id, short_name, user_name, user_age, user_mail, user_vk, user_tg, time_press))

    def get_supply(self, user_id, short_name):
        with self.connection:
            res = self.cursor.execute("SELECT user_id FROM volunteers WHERE user_id = ? AND short_name = ?", (user_id, short_name)).fetchone()
            return res

    def get_supply_username(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]

    def get_supply_userage(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_age FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]

    def get_supply_usermail(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_mail FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]

    def get_supply_uservk(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_vk FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]

    def get_supply_usertg(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT user_tg FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return res[0]

    def get_minage(self, event_name):
        with self.connection:
            res = self.cursor.execute("SELECT min_age FROM events WHERE full_text = ?", (event_name,)).fetchone()
            return res[0]

    def get_end_times(self, event_name):
        with self.connection:
            res = self.cursor.execute("SELECT end_time FROM events WHERE full_text = ?", (event_name,)).fetchone()
            return res[0]
