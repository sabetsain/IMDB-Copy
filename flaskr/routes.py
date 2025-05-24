from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from .db import get_db

bp = Blueprint('movies', __name__)

@bp.route('/movies')
def show_movies():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, title, year, director, genre, run_time, IMDB_rating, num_votes FROM movie")
        movies = cur.fetchall()
        column_names = [desc[0] for desc in cur.description] if cur.description else []
    return render_template('movies.html', movies=movies, column_names=column_names)

@bp.route('/actors')
def show_actors():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT actor_id, actor_name FROM actors")
        actors = cur.fetchall()
        column_names = [desc[0] for desc in cur.description] if cur.description else []
    return render_template('actors.html', actors=actors, column_names=column_names)

@bp.route('/watchlist')
def show_watchlist():
    user_id = session["username"]
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (user_id,))
        movie_ids = [row[0] for row in cur.fetchall()]
        if not movie_ids:
            movies = []
            column_names = []
        # format_strings = ','.join(['%s'] * len(movie_ids))
        movies = []
        for movie_id in movie_ids:
            cur.execute("""
                SELECT movie_id, title, year, director, genre, run_time, IMDB_rating, num_votes
                FROM movie
                WHERE movie_id = %s
            """, (movie_id,))
            movies += cur.fetchall()
        column_names = [desc[0] for desc in cur.description] if cur.description else []
    return render_template('watchlist_movies.html', movies=movies, column_names=column_names)



@bp.route('/add_rating', methods=['POST'])
def add_rating():
    user_id = session["username"]
    movie_id = request.form['movie_id']
    rating = request.form['rating']

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
        result = cur.fetchone()
        if result:
            imdb_rating, num_votes = result
            new_num_votes = num_votes + 1
            new_imdb_rating = (imdb_rating * num_votes + float(rating)) / (new_num_votes)
            cur.execute(
                "UPDATE movie SET IMDB_rating = %s, num_votes = %s WHERE movie_id = %s",
                (new_imdb_rating, new_num_votes, movie_id)
            )
            db.commit()

    return redirect(url_for(''))

@bp.route('/change_rating', methods=['POST'])
def change_rating():
    #user_id = session["UserName"]
    user_id = session["username"]
    movie_id = request.form['movie_id']
    rating = request.form['rating']

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "UPDATE rating SET rating = %s WHERE user_id = %s AND movie_id = %s",
            (rating, user_id, movie_id)
        )
        cur.execute(
            "SELECT IMDB_rating, num_votes FROM movie WHERE movie_id = %s",
            (movie_id,)
        )
        result = cur.fetchone()
        if result:
            imdb_rating, num_votes = result
            new_imdb_rating = (imdb_rating * num_votes - float(rating)) / (num_votes)
            cur.execute(
                "UPDATE movie SET IMDB_rating = %s WHERE movie_id = %s",
                (new_imdb_rating, movie_id)
            )
            db.commit()

    return redirect(url_for(''))

@bp.route('/delete_rating', methods=['POST'])
def delete_rating():
    user_id = session["username"]
    movie_id = request.form['movie_id']

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
        result = cur.fetchone()
        
        if result:
            imdb_rating, num_votes = result
            new_num_votes = num_votes - 1
            new_imdb_rating = (imdb_rating * num_votes) / (new_num_votes)
            cur.execute(
                "UPDATE movie SET IMDB_rating = %s, num_votes = %s WHERE movie_id = %s",
                (new_imdb_rating, new_num_votes, movie_id)
            )
            db.commit()

    return redirect(url_for(''))


@bp.route('/rating')
def show_rating():
    #user_id = session["UserName"]
    user_id = session['username']
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT movie_id, rating FROM rating WHERE user_id = %s", (user_id,))
        rating = cur.fetchall()
        column_names = [desc[0] for desc in cur.description] if cur.description else []
    return render_template('')


@bp.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    user_id = session.get("username")
    movie_id = request.form.get("movie_id")

    db = get_db()
    with db.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO watchlist (user_id, movie_id) VALUES (%s, %s)",
                (user_id, movie_id)
            )
            db.commit()
            flash("Movie added to watchlist!")
        except Exception as e:
            db.rollback()
            flash(f"Failed to add movie to watchlist: {e}")
    
    return redirect(url_for('movies.show_movies'))

@bp.route('/remove_from_watchlist', methods=['POST'])
def remove_from_watchlist():
    user_id = session.get("username")
    movie_id = request.form['movie_id']

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        db.commit()
    flash("Movie removed from watchlist!")
    return redirect(url_for('movies.show_watchlist'))