import os
import tempfile

import pytest

from bdl import create_app
from bdl.db import get_db, init_db

def sql_script():
	data_sql = None

	with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
		data_sql = f.read().decode("utf8")

	return data_sql

def fill_db(app):
	with app.app_context():
		db = get_db()
		db.executescript(sql_script())

@pytest.fixture
def app():
	db_handle, db_path = tempfile.mkstemp()
	app = create_app({
		"TESTING": True,
		"DATABASE": db_path
		})

	with app.app_context():
		init_db()

	yield app

	os.close(db_handle)
	os.unlink(app.config["DATABASE"])

@pytest.fixture
def client(app):
	with app.test_client() as client:
		yield client

@pytest.fixture
def cli_runner(app):
	return app.test_cli_runner()
