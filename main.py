from bs4 import BeautifulSoup
import requests as rq

def getsoup(s: str) -> BeautifulSoup:
    return BeautifulSoup(rq.get(s).text, 'html.parser')

soup = getsoup("https://www.millesima.fr/")

def nimportequoi() :
    links = soup.find_all('a')
    for link in links:
        print(link.get('href'))         