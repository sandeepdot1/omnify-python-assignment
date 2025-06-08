from db import get_db_connection, init_db
from datetime import datetime, timedelta, time


def seed_classes():
    init_db()

    conn = get_db_connection()
    cursor = conn.cursor()

    today = datetime.now().date()

    classes = [
        ("Yoga", "Alice", datetime.combine(today + timedelta(days=1), time(9, 0)), 10),
        ("Zumba", "Bob", datetime.combine(today + timedelta(days=2), time(18, 0)), 8),
        ("HIIT", "Charlie", datetime.combine(today + timedelta(days=3), time(6, 0)), 12),
    ]

    for name, instructor, dt, slots in classes:
        cursor.execute(
            "INSERT INTO fitness_classes (name, instructor, scheduled_at, available_slots) VALUES (?, ?, ?, ?)",
            (name, instructor, dt.strftime("%Y-%m-%d %H:%M:%S"), slots)
        )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_classes()
