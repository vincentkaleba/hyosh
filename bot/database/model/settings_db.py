import sqlite3
import threading
import logging

LOCK = threading.RLock()
LOGGER = logging.getLogger(__name__)

conn = sqlite3.connect('../database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subs_limit INTEGER DEFAULT 0,
    list_size INTEGER DEFAULT 25
)
''')
conn.commit()

class Settings:
    def __init__(self, subs_limit=0, list_size=25):
        self.subs_limit = subs_limit
        self.list_size = list_size

    def __repr__(self):
        return f'{self.id}'

def add_subs_limit(limit):
    with LOCK:
        cursor.execute('SELECT * FROM settings WHERE id = 1')
        settings = cursor.fetchall()
        if settings:
            cursor.execute('''
                UPDATE settings SET subs_limit = ? WHERE id = 1
            ''', (int(limit),))
            conn.commit()
        else:
            cursor.execute('''
                INSERT INTO settings (subs_limit)
                VALUES (?)
            ''', (int(limit),))
            conn.commit()

def add_list_size(size):
    with LOCK:
        cursor.execute('SELECT * FROM settings WHERE id = 1')
        settings = cursor.fetchall()
        if settings:
            cursor.execute('''
                UPDATE settings SET list_size = ? WHERE id = 1
            ''', (int(size),))
            conn.commit()
        else:
            cursor.execute('''
                INSERT INTO settings (list_size)
                VALUES (?)
            ''', (int(size),))
            conn.commit()

def get_settings():
    cursor.execute('SELECT * FROM settings WHERE id = 1')
    return cursor.fetchone()

def get_subscribers_limit():
    cursor.execute('SELECT subs_limit FROM settings WHERE id = 1')
    result = cursor.fetchone()
    return result[0] if result else 0

def get_list_size():
    cursor.execute('SELECT list_size FROM settings WHERE id = 1')
    result = cursor.fetchone()
    return result[0] if result else 25
