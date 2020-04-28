from bdl.db import get_db

def valid_code(code):
	db = get_db()
	return db.execute("SELECT codeVal FROM code WHERE codeVal=?", (code,)).fetchone() is not None

def add_code(code):
	db = get_db()
	db.execute("INSERT INTO code (codeVal) VALUES (?)", (code,))
	db.commit()

def remove_code(code):
	db = get_db()
	db.execute("DELETE FROM code WHERE codeVal=?", (code,))
	db.commit()
