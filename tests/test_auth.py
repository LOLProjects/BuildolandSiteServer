import uuid
from flask import session, g
from bdl.db import get_db
import pytest
from conftest import fill_db

def get_person(app, key, value):
	with app.app_context():
		db = get_db()
		return db.execute(f"SELECT * FROM user WHERE {key}='{value}'").fetchone()

def get_code(app, codeVal):
	with app.app_context():
		db = get_db()
		return db.execute(f"SELECT codeVal FROM code WHERE codeVal='{codeVal}'").fetchone()

def test_register_normal(app, client):
	fill_db(app)
	rv = client.get("/register")
	assert rv.status_code == 200
	assert b"Code" in rv.data

	data = {
	"code": "123-456-78",
	"username": "person",
	"email": "amrojjeh@gmail.com",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert rv.status_code == 302
	assert "http://localhost/" == rv.headers["Location"]
	
	code = get_code(app, "123-456-78")
	assert code is None

	person = get_person(app, "username", "person")
	assert person is not None
	assert person["username"] == "person"
	assert session["user_id"]== person["id"]

def test_register_wrong_code(app, client):
	fill_db(app)
	data = {
	"code": "124-456-78",
	"username": "person",
	"email": "amrojjeh@gmail.com",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert b"Invalid" in rv.data

	# User shan't be registered
	person = get_person(app, "username", "person")
	assert person is None

def test_register_no_code(app, client):
	fill_db(app)
	data = {
	"code": "",
	"username": "person",
	"email": "amrojjeh@gmail.com",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert b"Invalid" in rv.data

	# User shan't be registered
	person = get_person(app, "username", "person")
	assert person is None

def test_register_dup_user(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "test",
	"email": "amrojjeh@gmail.com",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert b"Username taken" in rv.data

	person = get_person(app, "email", "amrojjeh@gmail.com")
	assert person is None

	code = get_code(app, "123-456-78")
	assert code is not None

def test_register_no_user(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "",
	"email": "amrojjeh@gmail.com",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert b"Username is required" in rv.data

	person = get_person(app, "email", "amrojjeh@gmail.com")
	assert person is None

	code = get_code(app, "123-456-78")
	assert code is not None

def test_register_invalid_email(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "person",
	"email": "amrojjeh@gmail",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert b"Invalid email" in rv.data

	# User shan't be registered
	# Code shouldn't be deleted
	person = get_person(app, "email", "amrojjeh@gmail")
	assert person is None
	code = get_code(app, "123-456-78")
	assert code is not None

def test_register_invalid_email(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "person",
	"email": "amrojjeh@gmail",
	"password": "person"}

	rv = client.post("/register", data=data)
	assert b"Invalid email" in rv.data

	person = get_person(app, "email", "amrojjeh@gmail")
	assert person is None
	code = get_code(app, "123-456-78")
	assert code is not None

def test_register_same_uuid(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "person",
	"email": "amrojjeh@gmail.com",
	"password": "person"
	}

	with app.app_context():
		g.test_user_id = uuid.UUID(int=get_person(app, "username", "test")["id"])
		rv = client.post("/register", data=data)

		assert "http://localhost/" == rv.headers["Location"]
		
		code = get_code(app, "123-456-78")
		assert code is None

		person = get_person(app, "username", "person")
		assert person is not None
		assert person["username"] == "person"

		assert session["user_id"]== person["id"]
		assert person["id"] != get_person(app, "username", "test")["id"]

def test_register_no_pass(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "person",
	"email": "amrojjeh@gmail.com",
	"password": ""}

	rv = client.post("/register", data=data)
	assert b"Password is required" in rv.data

	person = get_person(app, "email", "amrojjeh@gmail.com")
	assert person is None
	code = get_code(app, "123-456-78")
	assert code is not None

# For things such as amrojjeh+bdl@gmail.com
def test_register_email_plus(app, client):
	fill_db(app)
	data = {
	"code": "123-456-78",
	"username": "person",
	"email": "amrojjeh+bdl@gmail.com",
	"password": "person"}

	rv = client.post("/register", data=data)

	person = get_person(app, "email", "amrojjeh+bdl@gmail.com")
	assert person is not None
	code = get_code(app, "123-456-78")
	assert code is None

def test_login_normal(app, client):
	fill_db(app)
	data = {
		"email": "test@test.com",
		"password":"test"
	}

	rv = client.get("/login")
	assert rv.status_code == 200
	assert b"Login" in rv.data

	rv = client.post("/login", data=data)
	assert rv.status_code == 302
	assert "http://localhost/" == rv.headers["Location"]

	rv = client.get("/")
	assert b"test" in rv.data
	assert b"Logout" in rv.data

def test_login_no_email(app, client):
	fill_db(app)
	data = {
		"email": "",
		"password": "test"
	}

	rv = client.post("/login", data=data)
	assert rv.status_code == 200
	assert b"Email required" in rv.data

def test_login_no_pass(app, client):
	fill_db(app)
	data = {
		"email": "test@test.com",
		"password": ""
	}

	rv = client.post("/login", data=data)
	assert rv.status_code == 200
	assert b"Password required" in rv.data

def test_login_wrong_pass(app, client):
	fill_db(app)
	data = {
		"email": "test@test.com",
		"password": "yoyoyo" # Actual pass: test
	}

	rv = client.post("/login", data=data)
	assert rv.status_code == 200
	assert b"Incorrect email or password" in rv.data

def test_login_wrong_email(app, client):
	fill_db(app)
	data = {
		"email": "notest@test.com", # Email is not registered
		"password": "test"
	}

	rv = client.post("/login", data=data)
	assert rv.status_code == 200
	assert b"Incorrect email or password" in rv.data

def test_logout(app, client):
	fill_db(app)

	data = {
		"email": "test@test.com",
		"password":"test"
	}

	client.post("/login", data=data)

	rv = client.get("/logout")
	assert rv.status_code == 302
	assert rv.headers["Location"] == "http://localhost/"

	rv = client.get("/")
	assert b"Login" in rv.data
