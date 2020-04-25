def test_register(client):
	rv = client.get("/register")
	assert b"Code" in rv.data

	# TEST ONCE CODES ARE IN
