from bdl.db import get_db, init_db
import sqlite3
import pytest

def test_init_db(app):
	with app.app_context():
		db = get_db()
		with pytest.raises(sqlite3.OperationalError) as e:
			db.execute("INSERT INTO user (email, username, password) VALUES ('test2@test2.com', 'test2', 'testpassword')")
			db.commit()
		init_db()
		db.execute("INSERT INTO user (email, username, password) VALUES ('test2@test2.com', 'test2', 'testpassword')")
		db.commit()

