import sqlite3
import threading
import logging

LOCK = threading.RLock()
LOGGER = logging.getLogger(__name__)

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji TEXT,
    set_top TEXT,
    set_bottom TEXT,
    set_caption TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS button (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    url TEXT
)
''')
conn.commit()

class Post:
    def __init__(self, emoji, set_top, set_bottom, set_caption):
        self.emoji = emoji
        self.set_top = set_top
        self.set_bottom = set_bottom
        self.set_caption = set_caption

    def __repr__(self):
        return f'{self.id}'

class Button:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'{self.id}'

def add_button(name, url):
    with LOCK:
        LOGGER.info(f"Button Added : {name} {url}")
        cursor.execute('''
            INSERT INTO button (name, url)
            VALUES (?, ?)
        ''', (name, url))
        conn.commit()

def delete_button():
    with LOCK:
        cursor.execute('DELETE FROM button')
        conn.commit()

def add_emoji(emoji):
    with LOCK:
        cursor.execute('SELECT * FROM post WHERE id=1')
        post = cursor.fetchone()
        if not post:
            cursor.execute('''
                INSERT INTO post (emoji, set_top, set_bottom, set_caption)
                VALUES (?, ?, ?, ?)
            ''', (emoji, None, None, None))
        else:
            cursor.execute('''
                UPDATE post SET emoji=? WHERE id=1
            ''', (emoji,))
        conn.commit()

def add_caption(caption):
    with LOCK:
        cursor.execute('SELECT * FROM post WHERE id=1')
        post = cursor.fetchone()
        if not post:
            cursor.execute('''
                INSERT INTO post (emoji, set_top, set_bottom, set_caption)
                VALUES (?, ?, ?, ?)
            ''', (None, None, None, caption))
        else:
            cursor.execute('''
                UPDATE post SET set_caption=? WHERE id=1
            ''', (caption,))
        conn.commit()

def add_top_text(text):
    with LOCK:
        cursor.execute('SELECT * FROM post WHERE id=1')
        post = cursor.fetchone()
        if not post:
            cursor.execute('''
                INSERT INTO post (emoji, set_top, set_bottom, set_caption)
                VALUES (?, ?, ?, ?)
            ''', (None, text, None, None))
        else:
            cursor.execute('''
                UPDATE post SET set_top=? WHERE id=1
            ''', (text,))
        conn.commit()

def add_bottom_text(text):
    with LOCK:
        cursor.execute('SELECT * FROM post WHERE id=1')
        post = cursor.fetchone()
        if not post:
            cursor.execute('''
                INSERT INTO post (emoji, set_top, set_bottom, set_caption)
                VALUES (?, ?, ?, ?)
            ''', (None, None, text, None))
        else:
            cursor.execute('''
                UPDATE post SET set_bottom=? WHERE id=1
            ''', (text,))
        conn.commit()

def get_buttons():
    cursor.execute('SELECT * FROM button')
    return cursor.fetchall()

def get_post():
    cursor.execute('SELECT * FROM post WHERE id=1')
    return cursor.fetchone()
