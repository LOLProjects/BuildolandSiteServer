def test_index(client):
	response = client.get("/")
	assert b"Buildoland Alpha" in response.data
	assert b"Register" in response.data and b"Login" in response.data

def test_index_logged_in(client):
	pass

def test_index_download(client):
	pass

def test_index_download_logged_in(client):
	pass
