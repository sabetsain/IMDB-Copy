from flask import Blueprint, render_template, session
from .db import get_db

bp = Blueprint('movies', __name__)

@bp.route('/movies')
def show_movies():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, title, year, director, genre, run_time, IMDB_rating, num_votes FROM movie")
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return render_template('movies.html', movies=movies, column_names=column_names)

@bp.route('/actors')
def show_actors():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT actor_id, actor_name FROM actors")
        actors = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return render_template('actors.html', actors=actors, column_names=column_names)

@bp.route('/watchlist')
def show_watchlist():
    #user_id = session["UserName"]
    user_id = "sebastian"
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (user_id,))
        movie_ids = [row[0] for row in cur.fetchall()]

        format_strings = ','.join(['%s'] * len(movie_ids))
        cur.execute(f"""
            SELECT movie_id, title, year, director, genre, run_time, IMDB_rating, num_votes
            FROM movie
            WHERE movie_id IN ({format_strings})
        """, tuple(movie_ids))
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    return render_template('watchlist_movies.html', movies=movies, column_names=column_names)
