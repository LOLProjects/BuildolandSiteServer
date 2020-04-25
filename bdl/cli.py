import click
from flask.cli import with_appcontext

from bdl.db import init_db, get_db


@click.command("init-db")
@with_appcontext
def init_db_command():
	init_db()
	click.echo("Initialized the database.")

@click.command("add-code")
@click.argument("codeval")
@with_appcontext
def add_code(codeval):
	db = get_db()
	if db.execute("SELECT codeVal from code WHERE codeVal=(?)", (codeval,)).fetchone() is not None:
		click.echo("Code already exists.")
		return
	db.execute("INSERT INTO code (codeVal) VALUES (?)", (codeval,))
	db.commit()

@click.command("list-codes")
@with_appcontext
def list_codes():
	db = get_db()
	codes = db.execute("SELECT codeVal FROM code").fetchall()
	for code in codes:
		click.echo(code["codeVal"])

@click.command("remove-code")
@click.argument("codeval")
@with_appcontext
def remove_code(codeval):
	db = get_db()
	code = db.execute("SELECT codeVal from code WHERE codeVal=?", (codeval,)).fetchone()
	if code is None:
		click.echo("Code doesn't exist.")
		return
	db.execute("DELETE FROM code WHERE codeVal=?", (codeval,))
	db.commit()
