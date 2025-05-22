import hashlib
import os

from .db import get_db

class User:
    def __init__(self, username=None, password=None):
        self.salt = "jfdalfjealkjtioraryimxcvkwngasvszefdasfwr12345678"
        self.username = username
        self.password = password

    def is_authenticated(self):
        db = get_db()

        if self.username is None:
            return False

        if self.password is None:
                return False
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            self.password.encode('utf-8'),
            self.salt.encode('utf-8'),
            100000
        ).hex()
    
        with db.cursor() as cur:
            cur.execute("SELECT password FROM user_profile WHERE user_id=%s", (self.username,))
            user_record = cur.fetchone()
            if user_record:
                stored_password = user_record
                return stored_password == hashed_password
            else:
                cur.execute("INSERT INTO user_profile(user_id, password) VALUES (%s, %s)", (self.username, hashed_password,))
                return True