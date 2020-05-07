from smtplib import SMTP_SSL
from email.message import EmailMessage

from flask import g, current_app

def get_smtp():
	if "smtp_server" in g:
		return g.smtp_server
	smtp_server = SMTP_SSL(current_app.config["SMTP"], port=465)
	smtp_server.login(current_app.config["EMAIL"], current_app.config["EMAIL_PASS"])
	g.smtp_server = smtp_server
	return g.smtp_server

def close_smtp(e=None):
	smtp_server = g.pop("smtp_server", None)
	if smtp_server:
		smtp_server.quit()

def send_email(to, subject, content):
	msg = EmailMessage()
	msg["Subject"] = subject
	msg["To"] = to
	msg["From"] = f"Buildoland <{current_app.config['EMAIL']}>"
	msg.set_content(content)
	get_smtp().send_message(msg)
