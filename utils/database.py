import sqlite3 as sq


class DatabaseManager:
    def __init__(self, db_name):
        self.db = sq.connect(db_name)
        self.cur = self.db.cursor()
        self.create_db()

    def create_db(self) -> None:
        try:
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS 'users' (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    tg_id TEXT
                )
            ''')
            self.db.commit()
        except sq.Error as Error:
            print('При создании таблицы возникла ошибка: ', Error)

    def create_user(self, first_name, last_name, tg_id):
        user = self.cur.execute('''
            SELECT 1 FROM users
            WHERE tg_id = ?
        ''', (tg_id,)).fetchone()

        if not user:
            self.cur.execute('''
                INSERT INTO users (first_name, last_name, tg_id) VALUES (?, ?, ?)
            ''', (first_name, last_name, tg_id))
            self.db.commit()

    def update_user(self, first_name, last_name, tg_id):
        self.cur.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?
            WHERE tg_id = ?
        ''', (first_name, last_name, tg_id,))

        self.db.commit()

    def select_user(self, tg_id):
        user = self.cur.execute('''
            SELECT * from users
            WHERE tg_id = ?
        ''', (tg_id,)).fetchone()

        return user

    def __del__(self):
        self.cur.close()
        self.db.close()
