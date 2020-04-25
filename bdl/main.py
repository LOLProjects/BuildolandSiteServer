from flask import Blueprint, g, session, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("main", __name__, url_prefix="")

@bp.route("/")
def index():
	return render_template("main/index.html")

@bp.route("/login")
def login():
	return render_template("main/login.html")

@bp.route("/register", methods=("GET", "POST"))
def register():
	if request.method == "GET":
		return render_template("main/register.html")
	code = request.form["code"]
	username = request.form["username"]
	password = request.form["password"]
	email = request.form["email"]

	# Check if code is in db
	# Remove code

	# Check if username is unique

	# Check if email is valid

	# Insert user

	# Save cookie

	# Make user global

	return redirect(url_for("main.index"))

@bp.route("/forgotPass")
def forgotPass():
	return render_template("main/forgotPass.html")
