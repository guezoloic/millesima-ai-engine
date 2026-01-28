from main import *

def test_soup():
    assert getsoup("https://example.com").find('h1').text == "Example Domain"
