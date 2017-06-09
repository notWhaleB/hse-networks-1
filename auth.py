import os
from hashlib import sha256
import sqlite3

_SALT_ = "&O*Y$B(&*#439/"
_N_ITER_ = 1024

conn = sqlite3.connect(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'passwd.sqlite3'
))

class UserExists(Exception):
    pass

class BadCredentials(Exception):
    pass

def _hash(passwd):
    hashed = passwd
    for _ in range(_N_ITER_):
        hashed = sha256(hashed + _SALT_).hexdigest()
    return hashed

def do_signup(user, passwd, email):
    cur = conn.cursor()
    cur.execute('SELECT hash FROM Users WHERE user=?', (user,))
    if cur.fetchone() is None:
        cur.execute('INSERT INTO Users VALUES (?, ?, ?)', (user, _hash(passwd), email))
    else:
        cur.close()
        raise UserExists
    cur.close()
    conn.commit()

def do_login(user, passwd):
    cur = conn.cursor()
    cur.execute('SELECT hash FROM Users WHERE user=?', (user,))
    res = cur.fetchone()
    if res is None or _hash(passwd) != res[0]:
        cur.close()
        raise BadCredentials
    cur.close()

