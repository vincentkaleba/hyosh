import sqlite3
import threading
import logging

LOCK = threading.RLock()
LOGGER = logging.getLogger(__name__)

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS channel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    channel_id BIGINT,
    subscribers INTEGER,
    channel_name TEXT,
    admin_username TEXT,
    description TEXT,
    invite_link TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ban_channel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id BIGINT
)
''')
conn.commit()

class Channel:
    def __init__(self, chat_id, channel_id, subscribers, channel_name, admin_username, description, invite_link):
        self.chat_id = chat_id
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.subscribers = subscribers
        self.admin_username = admin_username
        self.description = description
        self.invite_link = invite_link

    def __repr__(self):
        return '{}'.format(self.description)

class Ban:
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def __repr__(self):
        return f'{self.channel_id}'

def channel_data(chat_id, channel_id, channel_name, subscribers, admin_username, description, invite_link):
    with LOCK:
        LOGGER.info(f"New Channel {channel_id} [{channel_name}] by {admin_username}")
        cursor.execute('''
            INSERT INTO channel (chat_id, channel_id, channel_name, subscribers, admin_username, description, invite_link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chat_id, channel_id, channel_name, subscribers, admin_username, description, invite_link))
        conn.commit()

def is_channel_exist(channel_id):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM channel WHERE channel_id=?)', (channel_id,))
    return cursor.fetchone()[0]

def is_channel_ban(channel_id):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM ban_channel WHERE channel_id=?)', (channel_id,))
    return cursor.fetchone()[0]

def is_user_not_added_channel(chat_id):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM channel WHERE chat_id=?)', (chat_id,))
    return cursor.fetchone()[0]

def delete_channel(channel_id):
    with LOCK:
        LOGGER.info(f'Channel removed {channel_id}')
        cursor.execute('DELETE FROM channel WHERE channel_id=?', (channel_id,))
        conn.commit()

def get_all_channel(chat_id):
    cursor.execute('SELECT * FROM channel WHERE chat_id=?', (chat_id,))
    return cursor.fetchall()

def get_channel():
    cursor.execute('SELECT * FROM channel')
    return cursor.fetchall()

def update_subs(channel_id, subs):
    with LOCK:
        cursor.execute('UPDATE channel SET subscribers=? WHERE channel_id=?', (subs, channel_id))
        conn.commit()

def total_channel():
    cursor.execute('SELECT COUNT(*) FROM channel')
    return cursor.fetchone()[0]

def total_banned_channel():
    cursor.execute('SELECT COUNT(*) FROM ban_channel')
    return cursor.fetchone()[0]

def ban_channel(channel_id):
    with LOCK:
        cursor.execute('INSERT INTO ban_channel (channel_id) VALUES (?)', (channel_id,))
        conn.commit()
        LOGGER.info(f'Channel {channel_id} banned')

def unban_channel(channel_id):
    with LOCK:
        cursor.execute('DELETE FROM ban_channel WHERE channel_id=?', (channel_id,))
        conn.commit()

def is_channel_banned(channel_id):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM ban_channel WHERE channel_id=?)', (channel_id,))
    return cursor.fetchone()[0]

def get_channel_by_id(channel_id):
    cursor.execute('SELECT * FROM channel WHERE channel_id=?', (channel_id,))
    return cursor.fetchone()

def get_banned_channel_list():
    cursor.execute('SELECT channel_id FROM ban_channel')
    return [row[0] for row in cursor.fetchall()]

def get_user_channel_count(chat_id):
    cursor.execute('SELECT COUNT(*) FROM channel WHERE chat_id=?', (chat_id,))
    return cursor.fetchone()[0]

def chunck():
    cursor.execute('SELECT channel_id FROM channel')
    channel_ids = [row[0] for row in cursor.fetchall()]
    chunk_size = 100 
    for i in range(0, len(channel_ids), chunk_size):
        yield channel_ids[i:i+chunk_size]
