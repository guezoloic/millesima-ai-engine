from json import dumps
from bs4 import Tag
import pytest
from requests_mock import Mocker
from main import Scraper


@pytest.fixture(autouse=True)
def mock_site():
    with Mocker() as m:
        m.get(
            "https://www.millesima.fr/",
            text="<html><body><h1>MILLESIMA</h1></body></html>",
        )

        json_data = {
            "props": {
                "pageProps": {
                    "initialReduxState": {
                        "product": {
                            "content": {
                                "_id": "J4131/22-11652",
                                "partnumber": "J4131/22",
                                "productName": "Nino Negri : 5 Stelle Sfursat 2022",
                                "productNameForSearch": "Nino Negri : 5 Stelle Sfursat 2022",
                                "storeId": "11652",
                                "seoKeyword": "nino-negri-5-stelle-sfursat-2022.html",
                                "title": "Nino Negri : 5 Stelle Sfursat 2022",
                                "items": [
                                    {
                                        "_id": "J4131/22/C/CC/6-11652",
                                        "partnumber": "J4131/22/C/CC/6",
                                        "taxRate": "H",
                                        "listPrice": 390,
                                        "offerPrice": 390,
                                        "seoKeyword": "nino-negri-5-stelle-sfursat-2022-c-cc-6.html",
                                        "shortdesc": "Un carton de 6 Bouteilles (75cl)",
                                        "attributes": {
                                            "promotion_o_n": {
                                                "valueId": "0",
                                                "name": "En promotion",
                                                "value": "Non",
                                                "sequence": 80,
                                                "displayable": "False",
                                                "type": "CHECKBOX",
                                                "isSpirit": False,
                                            },
                                            "in_stock": {
                                                "valueId": "L",
                                                "name": "En stock",
                                                "value": "Livrable",
                                                "sequence": 65,
                                                "displayable": "true",
                                                "type": "CHECKBOX",
                                                "isSpirit": False,
                                            },
                                        },
                                        "stock": 12,
                                        "availability": "2026-02-05",
                                        "isCustomizable": False,
                                        "gtin_cond": "",
                                        "gtin_unit": "",
                                        "stockOrigin": "EUR",
                                        "isPrevSale": False,
                                    }
                                ],
                                "attributes": {
                                    "appellation": {
                                        "valueId": "433",
                                        "name": "Appellation",
                                        "value": "Sforzato di Valtellina",
                                        "url": "sforzato-di-valtellina.html",
                                        "isSpirit": False,
                                        "groupIdentifier": "appellation_433",
                                    },
                                    "note_rp": {
                                        "valueId": "91",
                                        "name": "Parker",
                                        "value": "91",
                                        "isSpirit": False,
                                    },
                                    "note_jr": {
                                        "valueId": "17",
                                        "name": "J. Robinson",
                                        "value": "17",
                                        "isSpirit": False,
                                    },
                                    "note_js": {
                                        "valueId": "93-94",
                                        "name": "J. Suckling",
                                        "value": "93-94",
                                        "isSpirit": False,
                                    },
                                },
                            }
                        }
                    }
                }
            }
        }

        html_product = f"""
        <html>
            <script id="__NEXT_DATA__" type="application/json">
                {dumps(json_data)}
            </script>
        </body>
        </html>
        """
        m.get(
            "https://www.millesima.fr/nino-negri-5-stelle-sfursat-2022.html",
            text=html_product,
        )

        # on return m sans fermer le server qui simule la page
        yield m


@pytest.fixture
def scraper() -> Scraper:
    return Scraper()


# EXO1
def test_soup(scraper: Scraper):
    h1: Tag | None = scraper.getsoup("").find("h1")
    assert isinstance(h1, Tag)
    assert h1.text == "MILLESIMA"


# EXO3
def test_appellation(scraper: Scraper):
    appellation = scraper.getjsondata("nino-negri-5-stelle-sfursat-2022.html")
    assert appellation.appellation() == "Sforzato di Valtellina"


# EXO4-5
def test_critiques(scraper: Scraper):
    critiques = scraper.getjsondata("nino-negri-5-stelle-sfursat-2022.html")
    assert critiques.parker() == "91"
    assert critiques.robinson() == "17"
    assert critiques.suckling() == "93.5"
