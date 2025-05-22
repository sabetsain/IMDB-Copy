import psycopg
import os
import click
from flask import current_app, g
from datetime import datetime
import csv
from flask import Flask

app = Flask(__name__)
def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(
            host="localhost",
            dbname="imdb_copy",
            user='dis_project',
            password='dis_project'
        )
        # g.db.row_factory = psycopg.rows
    return g.db

def load_movies_csv():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'Movies_Table.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with db.cursor() as cur:
            for row in reader:
                cur.execute(
                    "INSERT INTO movie (title, year, director, genre, run_time, IMDB_rating, num_votes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (row['title'], row['year'], row['director'], row['genre'], row['run_time'], row['IMDB_rating'], row['num_votes'])
                )
        db.commit()
def load_actors_csv():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'Actors_Table.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with db.cursor() as cur:
            for row in reader:
                cur.execute(
                    "INSERT INTO actors (actor_name) VALUES (%s)",
                    (row['actor_name'],)
                )
        db.commit()

def load_stars_in_csv():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'Stars_In_Table.csv'), newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with db.cursor() as cur:
            for row in reader:
                cur.execute(
                    "INSERT INTO stars_in (actor_id, movie_id) VALUES (%s, %s)",
                    (row['actor_id'], row['movie_id'])
                )
        db.commit()

def add_rating(user_id, movie_id, rating):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
            (user_id, movie_id, rating)
        )
        cur.execute(
            "SELECT IMDB_rating, num_votes FROM movie WHERE movie_id = %s",
            (movie_id,)
        )
        imdb_rating, num_votes = cur.fetchone()
        new_num_votes = num_votes + 1
        new_imdb_rating = (imdb_rating * num_votes + rating) / (new_num_votes)
        cur.execute(
            "UPDATE movie SET IMDB_rating = %s, num_votes = %s WHERE movie_id = %s",
            (new_imdb_rating, new_num_votes, movie_id)
        )
        db.commit()

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        with db.cursor() as cur:
            cur.execute(f.read().decode('utf8'))
        db.commit()
    load_movies_csv()
    load_actors_csv()
    load_stars_in_csv()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
