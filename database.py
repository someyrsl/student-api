import sqlite3

def get_connection():
    return sqlite3.connect("school.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            grade REAL
        )
    """)
    conn.commit()
    conn.close()