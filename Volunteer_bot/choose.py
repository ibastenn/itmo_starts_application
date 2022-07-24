import sqlite3


class Choose:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_all_events(self, user_id):
        with self.connection:
            a = []
            res = self.cursor.execute("SELECT short_name, full_text FROM events WHERE user_id = ?", (user_id,)).fetchall()
            for row in res:
                if row is not None:
                    a += [row]
            return a

    def get_base_volunteers(self, short_name, full_text):
        with self.connection:
            base = self.cursor.execute("SELECT basic FROM events WHERE short_name = ?", (short_name,)).fetchone()

            base_volunteers_list = [0]*base[0]
            if base is not None:
                count = base[0]
                all_users = self.cursor.execute("SELECT user_name, user_mail, user_vk, user_tg FROM volunteers WHERE short_name = ? ORDER BY time_press ASC",
                                               (full_text,)).fetchmany(count)
                for i in range(base[0]):
                    if i < len(all_users):
                        base_volunteers_list[i] = all_users[i]
            return base_volunteers_list

    def get_reserve_volunteers(self, short_name, full_text):
        with self.connection:
            base = self.cursor.execute("SELECT basic FROM events WHERE short_name = ?", (short_name,)).fetchone()
            reserve = self.cursor.execute("SELECT reserve FROM events WHERE short_name = ?", (short_name,)).fetchone()

            reserve_volunteers_list = [0]*reserve[0]
            if base is not None:
                count = base[0]
                if reserve is not None:
                    count += reserve[0]
                all_users = self.cursor.execute("SELECT user_name, user_mail, user_vk, user_tg FROM volunteers WHERE short_name = ? ORDER BY time_press ASC",
                                               (full_text,)).fetchmany(count)
                for i in range(base[0], count):
                    if i < len(all_users):
                        reserve_volunteers_list[i - base[0]] = all_users[i]
            return reserve_volunteers_list
