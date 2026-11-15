import sqlite3
from .config import DATA
def conn():
    c = sqlite3.connect(str(DATA / "app.db"), check_same_thread=False); c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, salt TEXT, pwhash TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS eval(id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER, cond TEXT, profile TEXT, truth INTEGER, system INTEGER, diff INTEGER, acc REAL, note TEXT)")
    return c
