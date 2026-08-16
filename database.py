import sqlite3
import json
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_roadmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_role TEXT,
            readiness_percent INTEGER,
            roadmap_json TEXT,
            status TEXT DEFAULT 'Not Started',
            saved_at TEXT
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


def save_roadmap(roadmap):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO career_roadmaps (target_role, readiness_percent, roadmap_json, saved_at)
        VALUES (?, ?, ?, ?)
    """, (
        roadmap["target_role"],
        roadmap["readiness_percent"],
        json.dumps(roadmap),
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()


def get_roadmaps():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, target_role, readiness_percent, roadmap_json, status, saved_at FROM career_roadmaps ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "target_role": r[1],
            "readiness_percent": r[2],
            "roadmap": json.loads(r[3]),
            "status": r[4],
            "saved_at": r[5],
        }
        for r in rows
    ]


def update_roadmap_status(roadmap_id, status):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE career_roadmaps SET status = ? WHERE id = ?", (status, roadmap_id))
    conn.commit()
    conn.close()


def delete_roadmap(roadmap_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM career_roadmaps WHERE id = ?", (roadmap_id,))
    conn.commit()
    conn.close()


def update_skill_status(roadmap_id, skill_name, status):
    """Update the status ('Not Started' | 'Learning' | 'Done' | 'Skip') for one skill
    inside a saved roadmap's JSON blob."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT roadmap_json FROM career_roadmaps WHERE id = ?", (roadmap_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return
    data = json.loads(row[0])
    for phase in data.get("phases", []):
        for skill in phase.get("skills", []):
            if skill["skill"] == skill_name:
                skill["status"] = status
    cursor.execute("UPDATE career_roadmaps SET roadmap_json = ? WHERE id = ?", (json.dumps(data), roadmap_id))
    conn.commit()
    conn.close()


def compute_completion_percent(roadmap):
    """% of skills marked Done, across phases that aren't the 'Already Have' group."""
    total = 0
    done = 0
    for phase in roadmap.get("phases", []):
        if phase.get("phase") == "Already Have":
            continue
        for skill in phase.get("skills", []):
            total += 1
            if skill.get("status") == "Done":
                done += 1
    return int((done / total) * 100) if total else 100