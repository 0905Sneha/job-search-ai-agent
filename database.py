import sqlite3
from datetime import datetime

DB_FILE = "career_app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            salary TEXT,
            link TEXT,
            status TEXT DEFAULT 'Saved',
            saved_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            experience TEXT,
            work_mode TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_job(job):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_jobs (title, company, location, salary, link, saved_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (job["title"], job["company"], job["location"], job["salary"], job["link"], datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    print("Saved job to DB:", job["title"])

def get_saved_jobs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, salary, link, status, saved_at FROM saved_jobs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    print("Rows found in saved__jons table:", len(rows))
    return rows

def update_status(job_id, status):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE saved_jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()

def delete_saved_job(job_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()

def save_preferences(location, experience, work_mode):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM preferences")  # keep only latest
    cursor.execute("INSERT INTO preferences (location, experience, work_mode) VALUES (?, ?, ?)",
                   (location, experience, work_mode))
    conn.commit()
    conn.close()

def get_preferences():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT location, experience, work_mode FROM preferences LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row