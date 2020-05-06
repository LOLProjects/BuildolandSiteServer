from email.message import EmailMessage
from base64 import urlsafe_b64encode

from flask import g, current_app, url_for
from bdl.email import get_smtp

# TODO: Get an actual email service with an actual address
def send_verification():
	msg = EmailMessage()
	msg["Subject"] = "Buildoland Verification"
	msg["From"] = f"Buildoland <{current_app.config['EMAIL']}>"
	msg["To"] = g.user.email
	url = current_app.config["DNS"] + url_for("auth.verify", token=urlsafe_b64encode(g.user.verif_token))
	msg.set_content(f"Click to the following to verify your email address: {url}")
	get_smtp().send_message(msg)
