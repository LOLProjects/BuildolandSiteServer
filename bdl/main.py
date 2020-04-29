from flask import Blueprint, render_template
from bdl.db import get_db

bp = Blueprint("main", __name__, url_prefix="")

# TODO: Email verificaiton!!
@bp.route("/profile")
def profile():
	return render_template("main/profile.html")

# TODO: Add download, make it login and verification required
@bp.route("/")
def index():
	return render_template("main/index.html")
