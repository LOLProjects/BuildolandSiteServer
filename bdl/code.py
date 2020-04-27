from bdl.db import get_db

def valid_code(code):
	db = get_db()
	return db.execute("SELECT codeVal FROM code WHERE codeVal=?", (code,)).fetchone() is not None

def delete_code(code):
	db = get_db()
	db.execute("DELETE FROM code WHERE codeVal=?", (code,))
	db.commit()
