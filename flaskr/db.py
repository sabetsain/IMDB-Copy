import os
import csv
import click
import psycopg
from flask import Flask
from flask import current_app, g
from flask.cli import with_appcontext

app = Flask(__name__)
pg_uri = "postgresql://dis_project:dis_project@db:5432/imdb_copy"

def get_db():
    """Get a database connection."""
    if 'db' not in g:
        g.db = psycopg.connect(pg_uri)
    return g.db

def load_movies_csv():
    """Load movies data from CSV into the database."""
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), 
                           '..', 'data', 'Movies_Table.csv'), 
                           newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with db.cursor() as cur:
            for row in reader:
                cur.execute(
                    "INSERT INTO movie (title, year, director, genre, " \
                    "run_time, IMDB_rating, num_votes, poster_url) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (row['title'], row['year'], row['director'], 
                     row['genre'], row['run_time'], row['IMDB_rating'], 
                     row['num_votes'], row['poster_url'])
                )
        db.commit()

def load_actors_csv():
    """Load actors data from CSV into the database."""
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), 
                           '..', 'data', 'Actors_Table.csv'),
                             newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with db.cursor() as cur:
            for row in reader:
                cur.execute(
                    "INSERT INTO actors (actor_name) VALUES (%s)",
                    (row['actor_name'],)
                )
        db.commit()

def close_db(e=None):
    """Close the database connection if it was opened."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initialize the database with the schema and load initial data."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        with db.cursor() as cur:
            cur.execute(f.read().decode('utf8'))
        db.commit()
    load_movies_csv()
    load_actors_csv()

def init_app(app):
    """Initialize the app with database functions."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
