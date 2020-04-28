import re
from uuid import uuid4
from flask import g
from werkzeug.security import generate_password_hash

from bdl.db import get_db
from bdl.code import valid_code, remove_code

class User:
	def __init__(self, id, email, username, hashed_password, code_used=None, verified=False):
		self.id = id
		self.email = email
		self.username = username
		self.hashed_password = hashed_password
		self.code_used = code_used
		self.verified = verified

class RegisterResult:
	SUCCESS = 0
	USERNAME_TAKEN = 1
	INVALID_EMAIL = 2
	INVALID_CODE = 3

# generates a new UUIDv4 for a new user
def new_uuid():
	db = get_db()
	# id = getattr(g, "test_user_id", None)
	# if id is None:
	id = uuid4()
	while (db.execute("SELECT id FROM user WHERE id=?", (id.bytes,)).fetchone() is not None):
		id = uuid4()
	return id

def get_user(id=None, email=None, username=None):
	db = get_db()
	user_row = None
	if id is None:
		if email is None:
			if username is None:
				return None
			else:
				user_row = db.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()
		else:
			user_row = db.execute("SELECT * FROM user WHERE email=?", (email,)).fetchone()
	else:
		user_row = db.execute("SELECT * FROM user WHERE id=?", (id,)).fetchone()

	return User(
		user_row["id"],
		user_row["email"],
		user_row["username"],
		user_row["password"],
		user_row["code_used"],
		user_row["verified"]) if user_row else None

def unique_username(username):
	return get_user(username=username) is None

# This is different than verifying the email
def valid_email(email):
	return re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*(\+[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9]+)*\.([a-z]{2,4})$", email) is not None

def add_user(email, username, hashed_password, code_used=None):
	user_id = new_uuid().bytes
	db = get_db()
	db.execute("INSERT INTO user (id, email, username, password, code_used) VALUES (?, ?, ?, ?, ?)",
		(user_id, email, username, hashed_password, code_used))
	db.commit()
	return User(user_id, email, username, hashed_password, code_used)

def register_user(email, username, password, code=None):
	"""Registers the user, returns (errorCode, user)"""
	if (not unique_username(username)):
		return (RegisterResult.USERNAME_TAKEN, None)

	if (not valid_email(email)):
		return (RegisterResult.INVALID_EMAIL, None)

	# TODO: Send a verification email
	# TODO: Start a test email server

	if (code is not None):
		if (not valid_code(code)):
			return (RegisterResult.INVALID_CODE, None)

		remove_code(code)

	hashed_password = generate_password_hash(password)
	user = add_user(email, username, hashed_password, code)
	return (RegisterResult.SUCCESS, user)