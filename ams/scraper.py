import requests
from bs4 import BeautifulSoup

# URL du site
url = "https://www.cert.ssi.gouv.fr/"

# Récupération du contenu de la page
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche du premier bloc "item" correspondant au rapport
    first_item = soup.find("div", class_="item cert-cti open")

    if first_item:
        # Recherche de la div qui contient la référence
        item_ref_name = first_item.find("div", class_="item-ref")
        if item_ref_name:
            # Récupération de la balise <a> et de son texte
            a_tag = item_ref_name.find("a")
            if a_tag:
                ref_text = a_tag.get_text(strip=True)
                print("La référence est :", ref_text)

else:
    print("Erreur lors de la requête :", response.status_code)
