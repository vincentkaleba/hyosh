import sqlite3
import threading
import logging

LOCK = threading.RLock()
LOGGER = logging.getLogger(__name__)

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS promo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel INTEGER,
    message_id INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS paid_promo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel INTEGER,
    message_id INTEGER
)
''')
conn.commit()

class Promo:
    def __init__(self, channel, message_id):
        self.channel = channel
        self.message_id = message_id

    def __repr__(self):
        return f'{self.id}'

class PaidPromo:
    def __init__(self, channel, message_id):
        self.channel = channel
        self.message_id = message_id

    def __repr__(self):
        return f'{self.id}'

def add_paidpromo(channel_id, message_id):
    with LOCK:
        LOGGER.info(f"Adding paid promo: Channel {channel_id}, Message ID {message_id}")
        cursor.execute('''
            INSERT INTO paid_promo (channel, message_id)
            VALUES (?, ?)
        ''', (channel_id, message_id))
        conn.commit()

def get_paidpromo():
    cursor.execute('SELECT * FROM paid_promo')
    return cursor.fetchall()

def delete_paid_promo():
    with LOCK:
        cursor.execute('DELETE FROM paid_promo')
        conn.commit()

def save_message_ids(channel_id, message_id):
    cursor.execute('SELECT * FROM promo WHERE channel=?', (channel_id,))
    promo = cursor.fetchall()
    if not promo:
        cursor.execute('''
            INSERT INTO promo (channel, message_id)
            VALUES (?, ?)
        ''', (channel_id, message_id))
        conn.commit()
    else:
        cursor.execute('''
            UPDATE promo SET message_id=? WHERE channel=?
        ''', (message_id, channel_id))
        conn.commit()

def get_promo():
    cursor.execute('SELECT * FROM promo')
    return cursor.fetchall()

def delete_promo():
    with LOCK:
        cursor.execute('DELETE FROM promo')
        conn.commit()
