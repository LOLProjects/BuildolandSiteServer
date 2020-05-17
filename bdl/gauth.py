# Gauth because it's game auth

from flask import Blueprint, request
from uuid import uuid4

bp = Blueprint("gauth", __name__, url_prefix="/gauth")

@bp.route("/start", methods=("POST",))
def start():
	return "aa44f915-50d2-4d19-bc87-f6dfcd4a1b5e".replace("-", "")

