from flask import Blueprint, request, jsonify
from .db import get_db
from .auth import generate_token, verify_token
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/movies', methods=['GET'])
def show_movies():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, poster_url, title, year, director, genre, run_time, IMDB_rating, num_votes FROM movie")
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'movies': movies, 'columns': column_names})

@bp.route('/actors', methods=['GET'])
def show_actors():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT actor_id, actor_name FROM actors")
        actors = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'actors': actors, 'columns': column_names})

@bp.route('/watchlist/<user_id>', methods=['GET'])
def show_watchlist(user_id):
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

@bp.route('/add_rating', methods=['POST'])
def add_rating():
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

@bp.route('/rating/<user_id>', methods=['GET'])
def show_rating(user_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, rating FROM rating WHERE user_id = %s", (user_id,))
        ratings = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return jsonify({'ratings': ratings, 'columns': column_names})

@bp.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
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


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
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
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT user_id FROM user_profile WHERE user_id=%s", (username,))
        if cur.fetchone():
            return jsonify({'success': False, 'error': 'User already exists'}), 409

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO user_profile (user_id, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
    return jsonify({'success': True, 'message': 'User registered successfully'})


def token_required(f):
    from functools import wraps
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
    return jsonify({'success': True, 'message': 'You are authorized'})