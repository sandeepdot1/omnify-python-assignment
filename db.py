import sqlite3
import os


def get_db_connection():
    db_path = os.getenv('DB_PATH', 'fitness_studio.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fitness_classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        instructor TEXT NOT NULL,
        scheduled_at TEXT NOT NULL,
        available_slots INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        client_name TEXT NOT NULL,
        client_email TEXT NOT NULL,
        FOREIGN KEY (class_id) REFERENCES fitness_classes (id)
    )
    ''')
    conn.commit()
    conn.close()
