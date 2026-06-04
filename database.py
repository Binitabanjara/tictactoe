import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'games.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            winner TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            player_name TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def save_game_result(player_name, winner, date):
    conn = get_db()
    conn.execute('INSERT INTO game_results (player_name, winner, date) VALUES (?, ?, ?)',
                 (player_name, winner, date))
    if winner == player_name:
        conn.execute('''
            INSERT INTO leaderboard (player_name, wins) VALUES (?, 1)
            ON CONFLICT(player_name) DO UPDATE SET wins = wins + 1
        ''', (player_name,))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    conn = get_db()
    rows = conn.execute('''
        SELECT player_name, wins FROM leaderboard
        ORDER BY wins DESC LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]