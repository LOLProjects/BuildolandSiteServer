import re
import sqlite3
from uuid import uuid4
from flask import Blueprint, g, session, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from bdl.db import get_db


bp = Blueprint("auth", __name__, url_prefix="")

# TODO: Add change password

# TODO: Finish login
@bp.route("/login")
def login():
	return render_template("auth/login.html")

# TODO: Refactor register
@bp.route("/register", methods=("GET", "POST"))
def register():
	if request.method == "GET":
		return render_template("auth/register.html")
	code = request.form["code"]
	username = request.form["username"]
	password = request.form["password"]
	email = request.form["email"]
	user_id = get_new_uuid().bytes
	errors = None

	db = get_db()

	# Check for empty values
	if (not username):
		flash("Username is required")
		return render_template("auth/register.html")

	if (not password):
		flash("Password is required")
		return render_template("auth/register.html")

	if (not email):
		flash("Email is required")
		return render_template("auth/register.html")

	# Check if username is unique
	user = db.execute("SELECT username FROM user WHERE username=?", (username,)).fetchone()
	if user is not None:
		flash("Username is taken")
		return render_template("auth/register.html")

	# Check if email is valid
	# TODO: Support emails capitals
	match = re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*(\+[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9]+)*\.([a-z]{2,4})$", email)
	if match is None:
		flash("Invalid email")
		return render_template("auth/register.html")

	# TODO: Send a verification email
	# Insert user

	# Check if code is in db
	# Remove code
	code_exists = db.execute("SELECT codeVal FROM code WHERE codeVal=?", (code,)).fetchone() is None
	if (code_exists):
		flash("Invalid code")
		return render_template("auth/register.html")

	db.execute("DELETE FROM code WHERE codeVal=?", (code,))
	db.commit()

	db.execute("INSERT INTO user (id, email, username, password, code_used) VALUES (?, ?, ?, ?, ?)",
		(user_id, email, username, generate_password_hash(password), code))
	db.commit()

	# Save cookie
	session["user_id"] = user_id

	return redirect(url_for("main.index"))

def get_new_uuid():
	db = get_db()
	id = getattr(g, "test_user_id", None)
	if id is None:
		id = uuid4()
	while (db.execute("SELECT id FROM user WHERE id=?", (id.bytes,)).fetchone() is not None):
		id = uuid4()
	return id

# TODO: Finish forgot pass
@bp.route("/forgotPass")
def forgotPass():
	return render_template("auth/forgotPass.html")
