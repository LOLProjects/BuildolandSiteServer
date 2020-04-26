import os
import colorama

from flask import Flask

colorama.init()

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_mapping(
		SECRET_KEY="dev",
		DATABASE=os.path.join(app.instance_path, "db.sqlite"))

	if test_config is None:
		app.config.from_pyfile("config.py", silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# print(colorama.Fore.RED + "Secret: " + app.config["SECRET_KEY"] + colorama.Style.RESET_ALL)

	# Add blueprints

	from . import main
	app.register_blueprint(main.bp)
	app.add_url_rule("/", endpoint="index")

	from . import auth
	app.register_blueprint(auth.bp)

	init_app(app)

	return app

def init_app(app):
	from . import db
	from . import cli
	app.teardown_appcontext(db.close_db)
	app.cli.add_command(cli.init_db_command)
	app.cli.add_command(cli.add_code)
	app.cli.add_command(cli.list_codes)
	app.cli.add_command(cli.remove_code)
