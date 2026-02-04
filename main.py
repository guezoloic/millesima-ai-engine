import requests
from typing import Any
from bs4 import BeautifulSoup
import json


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
        self._soup = self.getsoup()

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

        self._response: requests.Response = self._session.get(
            target_url, timeout=10)
        self._response.raise_for_status()

        return self._response

    def getsoup(self, subdir: str = "/") -> BeautifulSoup:
        """
        Docstring for getsoup

        :param self: Description
        :return: Description
        :rtype: BeautifulSoup
        """
        if subdir != None:
            self._request(subdir)
            self._soup = BeautifulSoup(self._response.text, "html.parser")
        return self._soup

    def get_json_data(self):
        script = self._soup.find("script", id="__NEXT_DATA__")
        if script and script.string:
            try:
                data: dict[str, Any] = json.loads(script.string)
                for element in ['props', 'pageProps', 'initialReduxState', 'product', 'content']:
                    data.get(element)
                return data
            except json.decoder.JSONDecodeError:
                pass
        return {}
