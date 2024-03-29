import re
import sqlite3
from functools import wraps
from base64 import urlsafe_b64encode

from flask import Blueprint, g, session, render_template, request, redirect, flash, url_for, current_app

from bdl.db import get_db
from bdl.email import send_email
from bdl.user import RegisterResult, register_user, get_user, change_user, valid_username, check_password_hash
from bdl.verification import send_verification

# TODO: verification_required wrapper

bp = Blueprint("auth", __name__, url_prefix="")

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get("user_id", None)
	if user_id is None:
		g.user = None
		return
	g.user = get_user(id=user_id)

def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwds):
		if (g.get("user")):
			return f(*args, **kwds)
		else:
			return redirect(url_for("auth.login", path=request.path))
	return wrapper

@bp.route("/login", defaults={"path":""}, methods=("GET", "POST"))
@bp.route("/login/<path:path>", methods=("GET", "POST"))
def login(path):
	def error(msg):
		flash(msg, "error")
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

	if path:
		return redirect("/" + path)

	return redirect(url_for("main.index"))

# TODO: Accept uppercase emails
@bp.route("/register", methods=("GET", "POST"))
def register():
	def error(msg):
		flash(msg, "error")
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

	error_code, user = register_user(email, username, password, code)
	if (error_code == RegisterResult.USERNAME_TAKEN):
		return error("Username taken")
	if (error_code == RegisterResult.EMAIL_TAKEN):
		return error("Email taken")
	if (error_code == RegisterResult.INVALID_EMAIL):
		return error("Invalid email")
	if (error_code == RegisterResult.INVALID_CODE):
		return error("Invalid code")
	if (error_code == RegisterResult.INVALID_USERNAME):
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

# TODO: On password change, change ID to log out of all devices
@bp.route("/change", methods=("GET", "POST"))
@login_required
def change():
	def error(message):
		flash(message, "error")
		return render_template("auth/change.html")

	if request.method == "GET":
		return render_template("auth/change.html")
	oldEmail = g.user.email

	username = request.form["username"]
	email = request.form["email"]
	oldPass = request.form["oldPass"]
	newPass = request.form["newPass"]


	emailChanged = email and email != g.user.email
	usernameChanged = username and username != g.user.username
	passChanged = newPass != oldPass
	# NOTE: For now, email can only be changed if it isn't verified
	if emailChanged and g.user.verified:
		return error("Email is verified")

	if (newPass or oldPass):
		if (not newPass):
			return error("New password is required")

		if (not oldPass):
			return error("Old password is required")

		if (not check_password_hash(g.user.hashed_password, oldPass)):
			return error("Incorrect password")

	error_code, _ = change_user(g.user, username, email, newPass)

	if (error_code == RegisterResult.USERNAME_TAKEN):
		return error("Username taken")
	if (error_code == RegisterResult.EMAIL_TAKEN):
		return error("Email taken")
	if (error_code == RegisterResult.INVALID_EMAIL):
		return error("Invalid email")
	if (error_code == RegisterResult.INVALID_USERNAME):
		return error("Invalid username")

	if (emailChanged):
		return redirect(url_for("auth.send_verif"))

	content = """
Your buildoland account has been updated recently. If you did not intend on these changes, please contact amrojjeh@gmail.com for support and change your password immediately.
	"""
	send_email(oldEmail, "Buildoland Account Change", content)

	return redirect(url_for("main.profile"))

@bp.route("/verify/<token>")
@login_required
def verify(token):
	if g.user.verified:
		return redirect(url_for("main.index"))
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
	flash("Verification sent", "success")
	return redirect(url_for("main.profile"))
