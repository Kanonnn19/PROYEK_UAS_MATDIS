import sqlite3
from datetime import datetime

DB_NAME = "passwords.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_password(password):

    conn = connect_db()
    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO password_history
    (password, created_at)
    VALUES (?, ?)
    """, (password, current_time))

    conn.commit()
    conn.close()


def get_history():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password, created_at
    FROM password_history
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


create_table()