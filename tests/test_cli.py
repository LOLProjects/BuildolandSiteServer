from bdl import cli
from bdl.db import get_db
from conftest import fill_db

def test_init_db_command(cli_runner):
	result = cli_runner.invoke(cli.init_db_command)
	assert "Error" not in result.output
	assert "Initialized the database." in result.output

def test_add_code_command(app, cli_runner):
	fill_db(app)
	result = cli_runner.invoke(cli.add_code_command, args=["SpecialCode"])
	assert "Error" not in result.output
	with app.app_context():
		db = get_db()
		code = db.execute("SELECT codeVal FROM code WHERE codeVal = 'SpecialCode'").fetchone()
		assert code is not None

def test_add_code_command_dup(app, cli_runner):
	fill_db(app)
	result = cli_runner.invoke(cli.add_code_command, args=["123-456-78"])
	assert "Error" not in result.output
	assert "already exists." in result.output

def test_list_codes_command(app, cli_runner):
	fill_db(app)
	result = cli_runner.invoke(cli.list_codes_command)
	assert "Error" not in result.output
	assert "123-456-78" in result.output

def test_remove_code_command(app, cli_runner):
	fill_db(app)
	result = cli_runner.invoke(cli.remove_code_command, args=["123-456-78"])
	assert "Error" not in result.output
	with app.app_context():
		db = get_db()
		code = db.execute("SELECT codeVal FROM code WHERE codeVal = '123-456-78'").fetchone()
		assert code is None

def test_remove_code_command_not_exist(cli_runner):
	result = cli_runner.invoke(cli.remove_code_command, args=["123-456-78"])
	assert "Error" not in result.output
	assert "doesn't exist" in result.output
