import re
import sqlite3
from flask import Blueprint, g, session, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from bdl.db import get_db
from bdl.user import RegisterResult, register_user

bp = Blueprint("auth", __name__, url_prefix="")

# TODO: Add change password

# TODO: Finish login
@bp.route("/login")
def login():
	return render_template("auth/login.html")

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
