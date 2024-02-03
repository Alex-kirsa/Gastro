import sqlite3
from datetime import datetime, timedelta
from config import REMINDER_SECS


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

    def check_user_in_db(self, user_id: str, username: str):
        user = self._select(f"SELECT * FROM users WHERE user_id='{user_id}'").fetchone()
        if user is None:
            self._request(
                f"INSERT INTO users(user_id, username) VALUES ('{user_id}', '{username}')"
            )

    def get_all_users(self):
        return self._select("SELECT user_id FROM users").fetchall()

    def get_all_mailings(self):
        return self._select("SELECT message_id, from_chat_id FROM mailings").fetchall()

    def insert_post(self, from_chat_id, message_id):
        self._request(
            f"INSERT INTO mailings (message_id, from_chat_id) VALUES ('{message_id}', '{from_chat_id}')"
        )

    def delete_user(self, user_id):
        self._request(f"DELETE FROM users WHERE user_id='{user_id}'")

    def update_datetime(self, user_id: str):
        self._request(
            f"UPDATE users SET last_action_datetime = '{datetime.now()}' WHERE user_id = {user_id}"
        )

    def get_users_out_of_datetime(self, datetime=datetime.now()):
        dtm = datetime.now() - timedelta(seconds=REMINDER_SECS)

        return self._select(
            f"SELECT user_id FROM users WHERE last_action_datetime <= '{dtm}'"
        ).fetchall()
