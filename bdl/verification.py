from email.message import EmailMessage
from base64 import urlsafe_b64encode

from flask import g, current_app, url_for, request
from bdl.email import send_email

def send_verification():
	url = request.url_root[:-1] + url_for("auth.verify", token=urlsafe_b64encode(g.user.verif_token))
	content = f"Click to the following to verify your email address: {url}"
	send_email(g.user.email, "Buildoland Verification", content)
