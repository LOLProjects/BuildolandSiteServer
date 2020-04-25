from bdl import cli

def test_init_db_command(cli_runner):
	result = cli_runner.invoke(cli.init_db_command)
	assert "Initialized the database." in result.output
