import re
from uuid import uuid4
from flask import g, current_app
# from werkzeug.security import generate_password_hash (Removed because salt can't be specified)
from hashlib import pbkdf2_hmac

from bdl.db import get_db
from bdl.code import valid_code, remove_code

class User:
	def __init__(self, id, email, username, hashed_password, code_used=None, verified=0, verif_token=None):
		self.id = id
		self.email = email
		self.username = username
		self.hashed_password = hashed_password
		self.code_used = code_used
		self.verified = verified
		self.verif_token = verif_token

class RegisterResult:
	SUCCESS = 0
	USERNAME_TAKEN = 1
	EMAIL_TAKEN = 2
	INVALID_EMAIL = 3
	INVALID_CODE = 4
	INVALID_USERNAME = 5

# generates a new UUIDv4 for a new user
def new_uuid():
	db = get_db()
	id = g.get("test_user_id")
	if not id:
		id = uuid4()
	while (db.execute("SELECT id FROM user WHERE id=?", (id.bytes,)).fetchone()):
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
		user_row["verified"],
		user_row["verif_token"]) if user_row else None

def generate_password_hash(password):
	return pbkdf2_hmac("sha256", password.encode(), current_app.config["SALT"], 150000).hex()

def check_password_hash(phash, password):
	return generate_password_hash(password) == phash

def unique_username(username):
	return get_user(username=username) is None

def unique_email(email):
	return get_user(email=email) is None

def valid_email(email):
	return re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*(\+[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9]+)*\.([a-z]{2,4})$", email) is not None

def valid_username(username):
	return re.match(r"[_0-9A-Za-z-]+$", username) is not None

def add_user(email, username, hashed_password, code_used=None):
	user_id = new_uuid().bytes
	verif_token = new_uuid().bytes
	db = get_db()
	db.execute("INSERT INTO user (id, email, username, password, code_used, verified, verif_token) VALUES (?, ?, ?, ?, ?, ?, ?)",
		(user_id, email, username, hashed_password, code_used, 0, verif_token))
	db.commit()
	return User(user_id, email, username, hashed_password, code_used, 0, verif_token)

# TODO: Use a fixed salt
def register_user(email, username, password, code=""):
	"""Registers the user, returns (errorCode, user)"""

	if (not valid_username(username)):
		return (RegisterResult.INVALID_USERNAME, None)

	if (not unique_username(username)):
		return (RegisterResult.USERNAME_TAKEN, None)

	if (not valid_email(email)):
		return (RegisterResult.INVALID_EMAIL, None)

	if (not unique_email(email)):
		return (RegisterResult.EMAIL_TAKEN, None)

	if (code):
		if (not valid_code(code)):
			return (RegisterResult.INVALID_CODE, None)

		remove_code(code)

	hashed_password = generate_password_hash(password)
	user = add_user(email, username, hashed_password, code)
	return (RegisterResult.SUCCESS, user)

def change_user(user, username="", email="", password="", verified=None):
	"""Change user details. If email gets changed, verified will automatically be 0"""

	if not verified:
		verified = g.user.verified

	if password:
		password = generate_password_hash(password)
	else:
		password = user.hashed_password

	if username and not valid_username(username):
		return (RegisterResult.INVALID_USERNAME, user)

	if username and not unique_username(username):
		return (RegisterResult.USERNAME_TAKEN, user)

	if not username:
		username = user.username

	if email and not valid_email(email):
		return (RegisterResult.INVALID_EMAIL, user)

	if not email:
		email = user.email
	else:
		verified = 0

	db = get_db()
	db.execute("UPDATE user SET username=?, email=?, password=?, verified=? WHERE id=?", (username, email, password, verified, user.id))
	db.commit()
	user.username = username
	user.email = email
	user.password = password
	user.verified = verified
	return (RegisterResult.SUCCESS, user)
