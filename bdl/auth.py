import re
import sqlite3
from flask import Blueprint, g, session, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash

from bdl.db import get_db
from bdl.user import RegisterResult, register_user, get_user

bp = Blueprint("auth", __name__, url_prefix="")

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get("user_id", None)
	if user_id is None:
		g.user = None
		return
	g.user = get_user(id=user_id)

@bp.route("/login", methods=("GET", "POST"))
def login():
	def error(msg):
		flash(msg)
		return render_template("auth/login.html")

	if request.method == "GET":
		return render_template("auth/login.html")
	email = request.form["email"].lower()
	password = request.form["password"]

	if (not email):
		return error("Email required")
	if (not password):
		return error("Password required")

	user = get_user(email=email)
	if user is None:
		return error("Incorrect email or password")

	if not check_password_hash(user.hashed_password, password):
		return error("Incorrect email or password")

	session["user_id"] = user.id

	return redirect(url_for("main.index"))

@bp.route("/register", methods=("GET", "POST"))
def register():
	def error(msg):
		flash(msg)
		return render_template("auth/register.html")

	if request.method == "GET":
		return render_template("auth/register.html")
	code = request.form["code"]
	username = request.form["username"]
	password = request.form["password"]
	email = request.form["email"].lower()

	# Check for empty values
	if (not username):
		return error("Username is required")

	if (not password):
		return error("Password is required")

	if (not email):
		return error("Email is required")

	errorCode, user = register_user(email, username, password, code)
	if (errorCode == RegisterResult.USERNAME_TAKEN):
		return error("Username taken")
	if (errorCode == RegisterResult.INVALID_EMAIL):
		return error("Invalid email")
	if (errorCode == RegisterResult.INVALID_CODE):
		return error("Invalid code")

	# Save cookie
	session["user_id"] = user.id

	return redirect(url_for("main.index"))

# TODO: Finish forgot pass
@bp.route("/forgotPass")
def forgotPass():
	return render_template("auth/forgotPass.html")

@bp.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("main.index"))
