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
	user_id = uuid4().bytes
	errors = None

	db = get_db()

	# Check if id exists
	while (db.execute("SELECT id FROM user WHERE id=?", (user_id,)).fetchone() is not None):
		user_id = uuid4().bytes

	# Check if username is unique
	user = db.execute("SELECT username FROM user WHERE username=?", (username,)).fetchone()
	if user is not None:
		flash("User already exists")
		return redirect(url_for("main.index"))

	# Check if email is valid
	match = re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*(\+[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9]+)*(\.[a-z]{2,4})$", email)

	if match is None:
		flash("Email syntax is not supported")
		return redirect(url_for("main.index"))

	# TODO: Send a verification email

	# Insert user
	db.execute("INSERT INTO user (id, email, username, password, code_used) VALUES (?, ?, ?, ?, ?)",
		(user_id, email, username, generate_password_hash(password), code))
	db.commit()

	# Check if code is in db
	# Remove code
	try:
		code = db.execute("DELETE FROM code WHERE codeVal=?", (code,))
	except sqlite3.OperationalError as e:
		flash("Code doesn't exist")
		return redirect(url_for("main.index"))

	db.commit()

	# Save cookie
	session["user_id"] = user_id

	return redirect(url_for("main.index"))

# TODO: Finish forgot pass
@bp.route("/forgotPass")
def forgotPass():
	return render_template("auth/forgotPass.html")
