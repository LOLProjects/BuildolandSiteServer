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

	print(colorama.Fore.RED + "Secret: " + app.config["SECRET_KEY"] + colorama.Style.RESET_ALL)

	from . import db
	db.init_app(app)

	from . import main
	app.register_blueprint(main.bp)
	app.add_url_rule("/", endpoint="index")

	return app
