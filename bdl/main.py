from flask import Blueprint, render_template
from bdl.db import get_db

bp = Blueprint("main", __name__, url_prefix="")

# TODO: Allow username change
# TODO: Add a profile page
@bp.route("/profile")
def profile():
	return "NOT YET DONE"

@bp.route("/")
def index():
	return render_template("main/index.html")
