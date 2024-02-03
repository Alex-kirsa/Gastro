import sqlite3

# from icecream import ic


class Database:
    def _connect(self):
        return sqlite3.connect("database/database.db")

    def _select(self, request: str):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute(request)
        return cur

    def _request(self, request: str):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute(request)
            con.commit()
        return

    def check_user_in_db(self, user_id: str):
        user = self._select(f"SELECT * FROM users WHERE user_id='{user_id}'").fetchone()
        if user is None:
            self._request(f"INSERT INTO users(user_id) VALUES ('{user_id}')")

    def get_all_users(self):
        return self._select("SELECT message_id, from_chat_id FROM mailings").fetchall()

    def get_all_mailings(self):
        return self._select("SELECT message_id, from_chat_id FROM mailings").fetchall()
