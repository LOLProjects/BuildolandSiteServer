from smtplib import SMTP_SSL

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
