DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS code;

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT UNIQUE NOT NULL,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
)

CREATE TABLE code(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	code TEXT UNQIUE
)
