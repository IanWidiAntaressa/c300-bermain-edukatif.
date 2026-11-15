"""Autentikasi: Admin (username+password, SQLite, PBKDF2) dan Guest (tanpa password, hanya-lihat)."""
import hashlib, secrets
from .db import conn
def _h(pw, salt): return hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), 150000).hex()
def ensure_default_admin(user="admin", pw="admin123"):
    with conn() as c:
        if not c.execute("SELECT 1 FROM users WHERE role='admin' LIMIT 1").fetchone():
            s = secrets.token_hex(16); c.execute("INSERT INTO users VALUES(?,?,?,?)", (user, s, _h(pw, s), "admin"))
def verify(user, pw):
    with conn() as c: r = c.execute("SELECT * FROM users WHERE username=? AND role='admin'", (user,)).fetchone()
    return bool(r) and secrets.compare_digest(r["pwhash"], _h(pw, r["salt"]))
def change_password(user, old, new):
    if len(new) < 6 or not verify(user, old): return False
    s = secrets.token_hex(16)
    with conn() as c: c.execute("UPDATE users SET salt=?, pwhash=? WHERE username=?", (s, _h(new, s), user))
    return True
