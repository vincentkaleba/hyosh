import sqlite3
import threading
import logging
import datetime

LOCK = threading.RLock()
LOGGER = logging.getLogger(__name__)

conn = sqlite3.connect('../database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    date DATE DEFAULT CURRENT_DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER
)
''')
conn.commit()

class User:
    def __init__(self, chat_id, first_name, last_name, username):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __repr__(self):
        return "<id {}>".format(self.chat_id)

class Admin:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return f'{self.chat_id}'

def add_user(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name if message.from_user.first_name else 'None'
    last_name = message.from_user.last_name if message.from_user.last_name else 'None'
    username = message.from_user.username if message.from_user.username else 'None'
    
    cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchall()
    
    with LOCK:
        if not user:
            cursor.execute('''
                INSERT INTO users (chat_id, first_name, last_name, username)
                VALUES (?, ?, ?, ?)
            ''', (chat_id, first_name, last_name, username))
            conn.commit()
            LOGGER.info('New User: chat_id {} username {}'.format(chat_id, username))
        else:
            cursor.execute('''
                UPDATE users 
                SET first_name = ?, last_name = ?, username = ? 
                WHERE chat_id = ?
            ''', (first_name, last_name, username, chat_id))
            conn.commit()

def delete_user(chat_id):
    with LOCK:
        cursor.execute('DELETE FROM users WHERE chat_id = ?', (chat_id,))
        conn.commit()

def get_admin():
    cursor.execute('SELECT chat_id FROM admins')
    return [admin[0] for admin in cursor.fetchall()]

def get_all():
    cursor.execute('SELECT chat_id FROM users')
    return [user[0] for user in cursor.fetchall()]

def add_admin(chat_id):
    with LOCK:
        cursor.execute('INSERT INTO admins (chat_id) VALUES (?)', (chat_id,))
        conn.commit()

def total_users():
    cursor.execute('SELECT COUNT(*) FROM users')
    return cursor.fetchone()[0]

def total_admin():
    cursor.execute('SELECT COUNT(*) FROM admins')
    return cursor.fetchone()[0]

def get_all_user_data():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def get_user_username(chat_id):
    cursor.execute('SELECT username FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    return result[0] if result else None
