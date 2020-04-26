from flask import Blueprint, render_template
from bdl.db import get_db

bp = Blueprint("main", __name__, url_prefix="")

# TODO: Get user_id from session before each request
# TODO: Allow username change

@bp.route("/")
def index():
	return render_template("main/index.html")
