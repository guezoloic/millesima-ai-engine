from main import *

scraper = Scraper()

def test_soup():
    assert scraper.getsoup().find('h1').text[3:12] == "MILLESIMA"
