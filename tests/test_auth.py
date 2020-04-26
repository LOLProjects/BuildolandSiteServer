from bdl.db import get_db
import pytest
from conftest import fill_db

def test_register_normal(app, client):
	fill_db(app)
	rv = client.get("/register")
	assert rv.status_code == 200
	assert b"Code" in rv.data

	data = {
	"code":"123-456-78",
	"username":"person",
	"email":"amrojjeh@gmail.com",
	"password":"person"}

	rv = client.post("/register", data=data)
	assert "http://localhost/" == rv.headers["Location"]
	
	with app.app_context():
		db = get_db()
		code = db.execute("SELECT codeVal FROM code WHERE codeVal='123-456-78'").fetchone()
		assert code is None
		person = db.execute("SELECT username FROM user WHERE username='person'").fetchone()
		assert person["username"] == "person"

# TODO: Add more tests

def test_register_wrong_code(client):
	pass

def test_register_dup(client):
	pass