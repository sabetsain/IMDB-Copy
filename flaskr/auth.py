import jwt
import datetime
from flask import current_app

def generate_token(username):
    """Generate a JWT token for a given username."""
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_token(token):
    """Verify a JWT token and return the username if valid, else None."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None