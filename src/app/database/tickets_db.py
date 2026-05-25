import sqlite3
from datetime import datetime
from .db import get_db

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER UNIQUE,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            topic TEXT NOT NULL,
            type TEXT,
            answers TEXT,
            status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL,
            closed_at TEXT,
            closed_by INTEGER,
            reason TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            total_applications INTEGER DEFAULT 0,
            accepted INTEGER DEFAULT 0,
            denied INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def save_ticket(channel_id, user_id, user_name, topic, ticket_type, answers, created_at):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO tickets 
        (channel_id, user_id, user_name, topic, type, answers, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'open')
    ''', (channel_id, user_id, user_name, topic, ticket_type, answers, created_at))
    conn.commit()
    conn.close()

def get_ticket(channel_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets WHERE channel_id = ?', (channel_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def delete_ticket(channel_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tickets WHERE channel_id = ?', (channel_id,))
    conn.commit()
    conn.close()

def update_ticket_status(channel_id, status, closed_by=None, reason=None):
    conn = get_db()
    cursor = conn.cursor()
    closed_at = datetime.now().isoformat()
    
    cursor.execute('''
        UPDATE tickets 
        SET status = ?, closed_at = ?, closed_by = ?, reason = ?
        WHERE channel_id = ?
    ''', (status, closed_at, closed_by, reason, channel_id))
    
    conn.commit()
    
    date = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('SELECT * FROM stats WHERE date = ?', (date,))
    existing = cursor.fetchone()
    
    if existing:
        if status == 'accepted':
            cursor.execute('''
                UPDATE stats 
                SET total_applications = total_applications + 1,
                    accepted = accepted + 1
                WHERE date = ?
            ''', (date,))
        else:
            cursor.execute('''
                UPDATE stats 
                SET total_applications = total_applications + 1,
                    denied = denied + 1
                WHERE date = ?
            ''', (date,))
    else:
        if status == 'accepted':
            cursor.execute('''
                INSERT INTO stats (date, total_applications, accepted, denied)
                VALUES (?, 1, 1, 0)
            ''', (date,))
        else:
            cursor.execute('''
                INSERT INTO stats (date, total_applications, accepted, denied)
                VALUES (?, 1, 0, 1)
            ''', (date,))
    
    conn.commit()
    conn.close()

def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM tickets')
    total = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "accepted"')
    accepted = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "denied"')
    denied = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM tickets WHERE status = "open"')
    open_count = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        SELECT date, total_applications, accepted, denied 
        FROM stats 
        ORDER BY date DESC 
        LIMIT 7
    ''')
    weekly = cursor.fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'accepted': accepted,
        'denied': denied,
        'open': open_count,
        'weekly': weekly
    }

def get_all_tickets(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tickets 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    results = cursor.fetchall()
    conn.close()
    return results