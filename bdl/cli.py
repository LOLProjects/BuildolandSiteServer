import click
from flask.cli import with_appcontext

from bdl.db import init_db


@click.command("init-db")
@with_appcontext
def init_db_command():
	init_db()
	click.echo("Initialized the database.")

@click.command("add-code")
@with_appcontext
def add_code():
	pass

@click.command("list-codes")
@with_appcontext
def list_codes():
	pass

@click.command("remove-code")
@with_appcontext
def remove_code(code_str):
	pass
