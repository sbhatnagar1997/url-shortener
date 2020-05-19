from urlshort import create_app


# Sample text to look for the 'Shorten' button 
def test_shorten(client):
    response = client.get('/')
    assert b'Shorten' in response.data

