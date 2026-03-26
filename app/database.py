
import sqlite3

DATABASE_URL = "fastapi.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row    # 결과를 dict처럼 접근 가능
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            price   REAL    NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


