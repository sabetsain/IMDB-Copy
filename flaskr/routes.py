import re
from .db import get_db
from functools import wraps
from flask import Blueprint, request, jsonify
from .auth import generate_token, verify_token
from werkzeug.security import generate_password_hash, check_password_hash

VALID_USERNAME = r'[_a-zA-Z0-9\.\-]+'
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/movies', methods=['GET'])
def show_movies():
    """
    Description
    -----------
    Retrieves all movies and their details from the database
    and returns them in JSON format.
    
    Parameters
    ----------
    None
    
    Returns 
    -------
    dict
        A JSON object containing a list of movies and their details.
        Each movie is represented by a tuple containing movie_id, poster_url,
        title, year, director, genre, run_time, IMDB_rating, and num_votes.
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, poster_url, title, year, " \
                    "director, genre, run_time, IMDB_rating, " \
                    "num_votes FROM movie")
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'movies': movies, 'columns': column_names})

@bp.route('/actors', methods=['GET'])
def show_actors():
    """
    Description
    -----------
    Fetch all actors from the database.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object containing a list of actors and their details.
        Each actor is represented by a tuple containing actor_id and actor_name.
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT actor_id, actor_name FROM actors")
        actors = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'actors': actors, 'columns': column_names})

@bp.route('/watchlist/<user_id>', methods=['GET'])
def show_watchlist(user_id):
    """
    Description
    -----------
    Fetch the watchlist for a specific user.

    This endpoint retrieves all movies in the user's watchlist
    and returns them in JSON format.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    dict
        A JSON object containing a list of movies and their details.
        If the user has no movies in their watchlist, it returns an empty list.
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (user_id,))
        movie_ids = [row[0] for row in cur.fetchall()]
        if not movie_ids:
            return jsonify({'movies': [], 'columns': []})
        format_strings = ','.join(['%s'] * len(movie_ids))
        cur.execute(f"""
            SELECT movie_id, poster_url, title, year, director, genre, run_time, IMDB_rating, num_votes
            FROM movie
            WHERE movie_id IN ({format_strings})
        """, tuple(movie_ids))
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'movies': movies, 'columns': column_names})

@bp.route('/favourite_actor/<user_id>', methods=['GET'])
def show_favourite_actor(user_id):
    """
    Description
    -----------
    Fetch the favourite actors for a specific user.
    Retrieves all favourite actors of the user
    and returns them in JSON format.
    
    Parameters
    ----------
    user_id : str
    
    Returns
    -------
    dict
        A JSON object containing a list of favourite actors and their details.
        Each actor is represented by a tuple containing actor_id and actor_name.
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT a.actor_id, a.actor_name
            FROM favourite_actor fa
            JOIN actors a ON fa.actor_id = a.actor_id
            WHERE fa.user_id = %s
        """, (user_id,))
        actors = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'actors': actors, 'columns': column_names})


@bp.route('/add_rating', methods=['POST'])
def add_rating():
    """
    Description
    -----------
    Adds a rating for a movie by a user.

    Parameters
    ----------
    Nonwe
    
    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    rating = float(data.get("rating"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO rating (user_id, movie_id, rating) VALUES (%s, %s, %s)",
            (user_id, movie_id, rating)
        )
        cur.execute(
            "SELECT IMDB_rating, num_votes FROM movie WHERE movie_id = %s",
            (movie_id,)
        )
        imdb_rating, num_votes = cur.fetchone()
        new_num_votes = num_votes + 1
        new_imdb_rating = (imdb_rating * num_votes + rating) / new_num_votes
        cur.execute(
            "UPDATE movie SET IMDB_rating = %s, num_votes = %s WHERE movie_id = %s",
            (new_imdb_rating, new_num_votes, movie_id)
        )
        db.commit()

    return jsonify({'success': True})

@bp.route('/change_rating', methods=['POST'])
def change_rating():
    """
    Description
    -----------
    Changes an existing rating for a movie by a user.
    
    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    new_rating = float(data.get("rating"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "UPDATE rating SET rating = %s WHERE user_id = %s AND movie_id = %s",
            (new_rating, user_id, movie_id)
        )
        db.commit()

    return jsonify({'success': True})

@bp.route('/delete_rating', methods=['POST'])
def delete_rating():
    """
    Description
    -----------
    Deletes a rating for a movie by a user.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "DELETE FROM rating WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        cur.execute(
            "SELECT IMDB_rating, num_votes FROM movie WHERE movie_id = %s",
            (movie_id,)
        )
        imdb_rating, num_votes = cur.fetchone()
        new_num_votes = num_votes - 1 if num_votes > 1 else 0
        new_imdb_rating = (imdb_rating * num_votes) / new_num_votes if new_num_votes > 0 else 0
        cur.execute(
            "UPDATE movie SET IMDB_rating = %s, num_votes = %s WHERE movie_id = %s",
            (new_imdb_rating, new_num_votes, movie_id)
        )
        db.commit()

    return jsonify({'success': True})

@bp.route('/rated_movies/<user_id>', methods=['GET'])
def show_rated_movies(user_id):
    """
    Description
    -----------
    Fetch all movies rated by a specific user.

    This endpoint retrieves all movies that the user has rated,
    including the user's rating and movie details.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    dict
        A JSON object containing a list of rated movies and their details.
        Each movie includes user_rating and movie information.
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT m.movie_id, m.poster_url, m.title, m.year, m.director, m.genre, m.run_time, 
                   m.IMDB_rating, m.num_votes, r.rating AS user_rating
            FROM rating r
            JOIN movie m ON r.movie_id = m.movie_id
            WHERE r.user_id = %s
        """, (user_id,))
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'movies': movies, 'columns': column_names})

@bp.route('/rating/<user_id>', methods=['GET'])
def show_rating(user_id):
    """
    Description
    -----------
    Fetch all ratings given by a specific user.

    This endpoint retrieves all movie ratings submitted by the user.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    dict
        A JSON object containing a list of movie IDs and their corresponding ratings.
    """
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, rating FROM rating WHERE user_id = %s", (user_id,))
        ratings = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'ratings': ratings, 'columns': column_names})

@bp.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    """
    Description
    -----------
    Adds a movie to a user's watchlist.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    if not user_id or not movie_id:
        return jsonify({'success': False, 'error': 'Missing user_id or movie_id'}), 400

    db = get_db()
    with db.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO watchlist (user_id, movie_id) VALUES (%s, %s)",
                (user_id, movie_id)
            )
            db.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/remove_from_watchlist', methods=['POST'])
def remove_from_watchlist():
    """
    Description
    -----------
    Removes a movie from a user's watchlist.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        db.commit()

    return jsonify({'success': True})

@bp.route('/add_favourite_actor', methods=['POST'])
def add_favourite_actor():
    """
    Description
    -----------
    Adds an actor to a user's list of favourite actors.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    actor_id = data.get("actor_id")
    if not user_id or not actor_id:
        return jsonify({'success': False, 'error': 'Missing user_id or actor_id'}), 400

    db = get_db()
    with db.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO favourite_actor (user_id, actor_id) VALUES (%s, %s)",
                (user_id, actor_id)
            )
            db.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/remove_favourite_actor', methods=['POST'])
def remove_favourite_actor():
    """
    Description
    -----------
    Removes an actor from a user's list of favourite actors.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the operation.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    actor_id = data.get("actor_id")

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "DELETE FROM favourite_actor WHERE user_id = %s AND actor_id = %s",
            (user_id, actor_id)
        )
        db.commit()

    return jsonify({'success': True})

@bp.route('/login', methods=['POST'])
def login():
    """
    Description
    -----------
    Authenticates a user and returns a JWT token if successful.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure, and a token if successful.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if (re.fullmatch(VALID_USERNAME, username) == None):
        return jsonify({'success': False, 'error': 'Invalid username format'}), 401
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT password FROM user_profile WHERE user_id=%s", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row[0], password):
            token = generate_token(username)
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401

@bp.route('/register', methods=['POST'])
def register():
    """
    Description
    -----------
    Registers a new user with a username and password.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating success or failure of the registration.
    """
    data = request.get_json()
    username = data.get('username')
    if (re.fullmatch(VALID_USERNAME, username) == None):
        return jsonify({'success': False, 'error': 'Invalid username format'}), 401
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT user_id FROM user_profile WHERE user_id=%s", (username,))
        if cur.fetchone():
            return jsonify({'success': False, 'error': 'User already exists'}), 409

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cur.execute("INSERT INTO user_profile (user_id, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
    return jsonify({'success': True, 'message': 'User registered successfully'})


def token_required(f):
    """
    Description
    -----------
    Decorator to require a valid JWT token for accessing a route.

    Parameters
    ----------
    f : function
        The route function to wrap.

    Returns
    -------
    function
        The wrapped function, which checks for a valid token before proceeding.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
        if not token or not verify_token(token):
            return jsonify({'success': False, 'error': 'Token is missing or invalid'}), 401
        return f(*args, **kwargs)
    return decorated


@bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    """
    Description
    -----------
    Example of a protected route that requires authentication.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A JSON object indicating the user is authorized.
    """
    return jsonify({'success': True, 'message': 'You are authorized'})