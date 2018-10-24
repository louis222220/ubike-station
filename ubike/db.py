import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


class SQLite3Database:
    def __init__(self):
        self.db = None

    def init_app(self, app):
        # app.teardown_appcontext(close_db)
        app.cli.add_command(self.init_db_command)
        self.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False
        )
        self.db.row_factory = sqlite3.Row

    def init_db(self):
        with current_app.open_resource('schema.sql') as f:
            self.db.executescript(f.read().decode('utf8'))

    @click.command('init-db')
    @with_appcontext
    def init_db_command(self):
        """Clear the existing data, create new tables and get stations data from ubike api."""
        self.init_db()
        click.echo('Initialized the database.')

sqlite = SQLite3Database()
