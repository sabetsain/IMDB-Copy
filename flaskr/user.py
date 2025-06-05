import hashlib
import os

from .db import get_db

class User:
    """
    Description
    -----------
    User class for handling user authentication and profile management.
    
    Attributes
    ----------
    username : str
        The username of the user.
    password : str
        The password of the user.
    salt : str
        A fixed salt used for hashing passwords.
    
    Methods
    -------
    is_authenticated() -> bool
        Checks if the user is authenticated by verifying the username and password.
        If the user does not exist, it creates a new user profile with the provided credentials.
    """

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
                stored_password = user_record[0]
                return stored_password == hashed_password
            else:
                cur.execute("INSERT INTO user_profile(user_id, password) VALUES (%s, %s)", (self.username, hashed_password,))
                db.commit()
                return True