import psycopg
import os
import click
from flask import current_app, g
from datetime import datetime

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
        # db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Removed as psycopg._psycopg.DateFromTicks is no longer available
# psycopg._psycopg.DateFromTicks = datetime.fromtimestamp