import click
from flask.cli import with_appcontext

from bdl.db import init_db, get_db
from bdl.code import valid_code, remove_code
# TODO: Add user, list users, and remove user

@click.command("init-db")
@with_appcontext
def init_db_command():
	init_db()
	click.echo("Initialized the database.")

# TODO: add-code should accept variadic arguments
@click.command("add-code")
@click.argument("codeval")
@with_appcontext
def add_code_command(codeval):
	db = get_db()
	if db.execute("SELECT codeVal from code WHERE codeVal=(?)", (codeval,)).fetchone() is not None:
		click.echo("Code already exists.")
		return
	db.execute("INSERT INTO code (codeVal) VALUES (?)", (codeval,))
	db.commit()

@click.command("list-codes")
@with_appcontext
def list_codes_command():
	count = 0
	db = get_db()
	codes = db.execute("SELECT codeVal FROM code").fetchall()
	for code in codes:
		click.echo(code["codeVal"])
		count += 1
	click.echo(f"There are {count} codes.")

@click.command("remove-code")
@click.argument("codeval")
@with_appcontext
def remove_code_command(codeval):
	if not valid_code(codeval):
		click.echo("Code doesn't exist.")
		return
	remove_code(codeval)

def add_commands(client):
	client.add_command(init_db_command)
	client.add_command(add_code_command)
	client.add_command(list_codes_command)
	client.add_command(remove_code_command)
