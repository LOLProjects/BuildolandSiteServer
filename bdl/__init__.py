import os

from flask import Flask


# TODO: Update colors and background
# TODO: Add auth system for the actual game

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


	# Add blueprints

	from . import main
	app.register_blueprint(main.bp)
	app.add_url_rule("/", endpoint="index")

	from . import auth
	app.register_blueprint(auth.bp)

	init_app(app)

	return app

def init_app(app):
	from . import cli
	app.teardown_appcontext(teardown_appcontext)
	cli.add_commands(app.cli)

def teardown_appcontext(e=None):
	from . import db
	from . import email
	db.close_db()
	email.close_smtp()

