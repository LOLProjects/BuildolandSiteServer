from bdl import cli
from bdl.db import get_db

def test_init_db_command(cli_runner):
	result = cli_runner.invoke(cli.init_db_command)
	assert "Error" not in result.output
	assert "Initialized the database." in result.output

def test_add_code_command(appWdata, cli_runner):
	result = cli_runner.invoke(cli.add_code, args=["SpecialCode"])
	assert "Error" not in result.output
	with appWdata.app_context():
		db = get_db()
		code = db.execute("SELECT codeVal FROM code WHERE codeVal = 'SpecialCode'").fetchone()
		assert code is not None

def test_add_code_command_dup(appWdata, cli_runner):
	result = cli_runner.invoke(cli.add_code, args=["123-456-78"])
	assert "Error" not in result.output
	assert "already exists." in result.output

def test_list_codes_command(cli_runnerWdata):
	result = cli_runnerWdata.invoke(cli.list_codes)
	assert "Error" not in result.output
	assert "123-456-78" in result.output

def test_remove_code_command(appWdata, cli_runnerWdata):
	result = cli_runnerWdata.invoke(cli.remove_code, args=["123-456-78"])
	assert "Error" not in result.output
	with appWdata.app_context():
		db = get_db()
		code = db.execute("SELECT codeVal FROM code WHERE codeVal = '123-456-78'").fetchone()
		assert code is None

def test_remove_code_command_not_exist(cli_runner):
	result = cli_runner.invoke(cli.remove_code, args=["123-456-78"])
	assert "Error" not in result.output
	assert "doesn't exist" in result.output
