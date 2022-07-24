import sqlite3

class DBA:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id,)).fetchone()

    def add_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO admins (user_id) VALUES (?)", (user_id,))

    # статус активности
    def get_statA(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT status FROM admins WHERE user_id = ?", (user_id,)).fetchone()
            if result is not None:
                status = result[0]
            else:
                status = ""
            return status

    def clean_empty_events(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM events WHERE user_id = ? AND short_name is NULL", (user_id,))

    def delete_all_active(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM events WHERE user_id = ? AND active = 1", (user_id,))

    def add_admin_to_events(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO events (user_id) VALUES (?)", (user_id,))

    def set_shortname(self, user_id, short_name):
        with self.connection:
            return self.cursor.execute("UPDATE events SET short_name = ? WHERE user_id = ? AND active = 1", (short_name, user_id,))

    def set_limit(self, user_id, limit):
        with self.connection:
            return self.cursor.execute("UPDATE events SET `limit` = ? WHERE user_id = ? AND active = 1", (limit, user_id,))

    def set_basic(self, user_id, basic):
        with self.connection:
            return self.cursor.execute("UPDATE events SET basic = ? WHERE user_id = ? AND active = 1", (basic, user_id,))

    def set_reversed(self, user_id, reserved):
        with self.connection:
            return self.cursor.execute("UPDATE events SET reserve = ? WHERE user_id = ? AND active = 1", (reserved, user_id,))

    def set_full_text_of_new_event(self, user_id, full_text):
        with self.connection:
            return self.cursor.execute("UPDATE events SET full_text = ? WHERE user_id = ? AND active = 1", (full_text, user_id,))

    def set_min_age(self, user_id, min_age):
        with self.connection:
            return self.cursor.execute("UPDATE events SET min_age = ? WHERE user_id = ? AND active = 1", (min_age, user_id,))

    def set_statA(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE admins SET status = ? WHERE user_id = ? AND active = 1", (status, user_id,))

    def set_PostTime(self, user_id, time_create):
        with self.connection:
            return self.cursor.execute("UPDATE events SET time_create = ? WHERE user_id = ? AND active = 1", (time_create, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM events WHERE user_id = ? AND active = 1", (user_id,)).fetchone()
            if result is not None:
                print("get_signup = " + result[0])
                signup = result[0]
            else:
                signup = ""
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE events SET signup = ? WHERE user_id = ? AND active = 1", (signup, user_id,))

    def set_active_done(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE events SET active = 0 WHERE user_id = ? AND active = 1", (user_id,))

    def ending_time(self, user_id):
        with self.connection:
            limit_t = self.cursor.execute("SELECT `limit` FROM events WHERE user_id = ? AND active = 1", (user_id,)).fetchone()
            limit_split = limit_t[0].split('.')
            limit_time = int(limit_split[0]) * 24 * 60 * 60 * 1000 + int(limit_split[1]) * 60 * 60 * 1000\
                         + int(limit_split[2]) * 60 * 1000 + int(limit_split[3]) * 1000
            first_time = self.cursor.execute("SELECT time_create FROM events WHERE user_id = ? AND active = 1", (user_id,)).fetchone()
            end_time = 0
            if first_time is not None and first_time[0] is not None:
                end_time = first_time[0] + limit_time
            return self.cursor.execute("UPDATE events SET end_time = ? WHERE user_id = ? AND active = 1", (end_time, user_id,))
