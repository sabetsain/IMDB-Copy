import jwt
import datetime
from flask import current_app

def generate_token(username):
    """
    Description
    -----------
    This function generates a JWT token for the given username.
    The token is valid for 24 hours.

    Parameters
    ----------
    username : str
        The username for which the token is generated.
    Returns
    -------
    str
        The generated JWT token as a string.
    """

    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_token(token):
    """
    Description
    -----------
    This function verifies the JWT token and returns the username if valid.
    If the token is expired or invalid, it returns None.
    
    Parameters
    ----------
    token : str
        The JWT token to verify.

    Returns
    -------
    str or None
        The username if the token is valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None