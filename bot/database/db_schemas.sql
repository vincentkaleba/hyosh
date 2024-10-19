CREATE TABLE IF NOT EXISTS channel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    channel_id BIGINT,
    subscribers INTEGER,
    channel_name TEXT,
    admin_username TEXT,
    description TEXT,
    invite_link TEXT
);

CREATE TABLE IF NOT EXISTS ban_channel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id BIGINT
);

CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji TEXT,
    set_top TEXT,
    set_bottom TEXT,
    set_caption TEXT
);

CREATE TABLE IF NOT EXISTS button (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    url TEXT
);

CREATE TABLE IF NOT EXISTS promo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel INTEGER,
    message_id INTEGER
);

CREATE TABLE IF NOT EXISTS paid_promo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel INTEGER,
    message_id INTEGER
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subs_limit INTEGER DEFAULT 0,
    list_size INTEGER DEFAULT 25
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER
);
