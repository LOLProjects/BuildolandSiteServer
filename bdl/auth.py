import re
import sqlite3
from functools import wraps
from base64 import urlsafe_b64encode

from flask import Blueprint, g, session, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash

from bdl.db import get_db
from bdl.email import get_smtp
from bdl.user import RegisterResult, register_user, get_user, change_user, valid_username
from bdl.verification import send_verification

# TODO: Organize flashes with categories
# TODO: verification_required wrapper

bp = Blueprint("auth", __name__, url_prefix="")

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get("user_id", None)
	if user_id is None:
		g.user = None
		return
	g.user = get_user(id=user_id)

# TODO: Redirect to old url with the same parameters
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwds):
		if (g.get("user")):
			return f(*args, **kwds)
		else:
			return redirect(url_for("auth.login"))
	return wrapper

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
		return error("Email is required")
	if (not password):
		return error("Password is required")

	user = get_user(email=email)
	if user is None:
		return error("Incorrect email or password")

	if not check_password_hash(user.hashed_password, password):
		return error("Incorrect email or password")

	session["user_id"] = user.id

	return redirect(url_for("main.index"))

# TODO: Accept uppercase emails
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
	if (not code):
		return error("Code is required")

	if (not username):
		return error("Username is required")

	if (not password):
		return error("Password is required")

	if (not email):
		return error("Email is required")

	errorCode, user = register_user(email, username, password, code)
	if (errorCode == RegisterResult.USERNAME_TAKEN):
		return error("Username taken")
	if (errorCode == RegisterResult.EMAIL_TAKEN):
		return error("Email taken")
	if (errorCode == RegisterResult.INVALID_EMAIL):
		return error("Invalid email")
	if (errorCode == RegisterResult.INVALID_CODE):
		return error("Invalid code")
	if (errorCode == RegisterResult.INVALID_USERNAME):
		return error("Invalid username")

	# Save cookie
	session["user_id"] = user.id
	return redirect(url_for("auth.send_verif"))

# TODO: Finish forgot pass
@bp.route("/forgotPass")
def forgotPass():
	return render_template("auth/forgotPass.html")

@bp.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("main.index"))

# TODO: Change email address, after verif is done
# TODO: Refactor change here and in user.py
# TODO: Check if username is unique
@bp.route("/change", methods=("GET", "POST"))
@login_required
def change():
	def error(message):
		flash(message)
		return render_template("auth/change.html")

	if request.method == "GET":
		return render_template("auth/change.html")

	username = request.form["username"]
	oldPass = request.form["oldPass"]
	newPass = request.form["newPass"]

	if (username and not valid_username(username)):
		return error("Invalid username")

	if (newPass or oldPass):
		if (not newPass):
			return error("New password is required")

		if (not oldPass):
			return error("Old password is required")

		if (not check_password_hash(g.user.hashed_password, oldPass)):
			return error("Incorrect password")

	change_user(g.user, username, newPass)
	return redirect(url_for("main.profile"))

@bp.route("/verify/<token>")
@login_required
def verify(token):
	if urlsafe_b64encode(g.user.verif_token) != token.encode():
		flash("Could not verify, please login to the correct account before verifying", "error")
	else:
		change_user(g.user, verified=1)
		flash("You've been verified!", "success")
	return redirect(url_for("main.index"))

@bp.route("/sendverif")
@login_required
def send_verif():
	send_verification()
	flash("Verification sent")
	return redirect(url_for("main.profile"))
