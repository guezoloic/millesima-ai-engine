import requests
from typing import Any
from bs4 import BeautifulSoup
import json

url = "louis-latour-aloxe-corton-1er-cru-les-chaillots-2018.html"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')


class MillesimaSoup(BeautifulSoup):
    def __init__(self, markup="", features="html.parser", *args, **kwargs):
        super().__init__(markup, features, *args, **kwargs)
        
        self._json_data = self._extract_json_data()

    def _extract_json_data(self) -> dict[str, Any]:
        script = self.find("script", id="__NEXT_DATA__")

        if script and script.string:
            try:
                data: dict[str, Any] = json.loads(script.string)
                for element in ['props', 'pageProps', 'initialReduxState', 'product', 'content']:
                    data.get(element)
                return data
            except json.decoder.JSONDecodeError:
                return {}
        return {}


class Scraper:
    """
    Scraper est une classe qui permet de gerer 
    de façon dynamique des requetes uniquement 
    sur le serveur https de Millesina
    """

    def __init__(self):
        """
        Docstring for __init__

        :param self: Description
        :param subdir: Description
        :type subdir: str
        """
        # Très utile pour éviter de renvoyer toujours les mêmes handshake
        # TCP et d'avoir toujours une connexion constante avec le server
        self._session: requests.Session = requests.Session()
        self._url: str = "https://www.millesima.fr/"
        self._soup = None

    def _request(self, subdir: str, use_cache: bool = True) -> requests.Response | requests.HTTPError:
        """
        Docstring for _request

        :param self: Description
        :param subdir: Description
        :type subdir: str
        :param use_cache: Description
        :type use_cache: bool
        :return: Description
        :rtype: Response | AttributeError
        """

        target_url: str = f"{self._url}{subdir.lstrip("/")}"

        # Éviter un max possible de faire des requetes au servers même
        # en ayant un tunnel tcp avec le paramètre `use_cache` que si
        # activer, va comparer l'url avec l'url précédant
        if use_cache and hasattr(self, "_response") and self._response is not None:
            if self._response.url == target_url:
                return self._response

        self._response: requests.Response = self._session.get(target_url, timeout=10)
        self._response.raise_for_status()

        return self._response
    

    def getsoup(self, subdir: str = "/") -> BeautifulSoup:
        """
        Docstring for getsoup

        :param self: Description
        :return: Description
        :rtype: BeautifulSoup
        """
        self._request(subdir)
        self._soup = BeautifulSoup(self._response.text, "html.parser")
        return self._soup
    
    


print(Scraper().getsoup(url))

# # On cible la balise magique
# script_tag = soup.find('script', id='__NEXT_DATA__')
# print(script_tag)

# if script_tag:
#     # On transforme le texte en vrai dictionnaire Python
#     data = json.loads(script_tag.string)
#     # Navigation dans l'objet (Next.js structure toujours comme ça)
#     product_info = data['props']['pageProps']['initialReduxState']['product']['content']

#     print(f"Vin : {product_info['productName']}")
#     print(f"Prix HT : {product_info['items'][0]['htPrice']} €")
#     print(f"Stock : {product_info['items'][0]['stock']}")
