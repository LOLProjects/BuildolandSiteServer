from flask import Blueprint, render_template
from bdl.db import get_db

bp = Blueprint("main", __name__, url_prefix="")

# TODO: Allow username change
# TODO: Allow password change
# TODO: Email verificaiton!!
@bp.route("/profile")
def profile():
	return render_template("main/profile.html")

@bp.route("/")
def index():
	return render_template("main/index.html")
