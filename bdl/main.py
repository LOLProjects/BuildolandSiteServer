from flask import Blueprint, g, session, render_template

bp = Blueprint("main", __name__, url_prefix="")

@bp.route("/")
def index():
	return render_template("main/index.html")

@bp.route("/login")
def login():
	return render_template("main/login.html")

@bp.route("/register")
def register():
	return render_template("main/register.html")

@bp.route("/forgotPass")
def forgotPass():
	return render_template("main/forgotPass.html")

