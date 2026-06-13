import sqlite3
import datetime
def init_db():
    conn = sqlite3.connect('music_server.db',timeout=10.0)
    c = conn.cursor()
    c.execute('PRAGMA journal_mode=WAL;')
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
          uid INTEGER PRIMARY KEY,
          username TEXT NOT NULL,
          password TEXT NOT NULL
    )
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS Tracks (
          tid INTEGER PRIMARY KEY,
          title TEXT NOT NULL,
          artist TEXT
    ) 
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS Playlists (
          pid  INTEGER PRIMARY KEY,
          uid  INTEGER NOT NULL,
          name TEXT NOT NULL,
          FOREIGN KEY(uid) REFERENCES Users(uid)
          )
    ''')
    c.execute(''' CREATE TABLE IF NOT EXISTS UserState(
            uid TEXT PRIMARY KEY,
            username TEXT,
            ip_address TEXT,
            last_seen TIMESTAMP,
            is_active INTEGER DEFAULT 1)
''')
    c.execute('''CREATE TABLE IF NOT EXISTS ActiveBans(
            ip_address TEXT PRIMARY KEY,
            ban_timestamp TEXT,
            expires_at TEXT
              )''')
    conn.commit()
    conn.close()
if  __name__== "__main__":
    init_db()
