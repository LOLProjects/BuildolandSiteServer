from email.message import EmailMessage
from base64 import urlsafe_b64encode

from flask import g, current_app, url_for, request
from bdl.email import get_smtp

def send_verification():
	msg = EmailMessage()
	msg["Subject"] = "Buildoland Verification"
	msg["From"] = f"Buildoland <{current_app.config['EMAIL']}>"
	msg["To"] = g.user.email
	url = request.url_root[:-1] + url_for("auth.verify", token=urlsafe_b64encode(g.user.verif_token))
	msg.set_content(f"Click to the following to verify your email address: {url}")
	get_smtp().send_message(msg)
