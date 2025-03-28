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

        # Extraction de la date
        date_span = first_item.find("span", class_="item-date")
        date_text = date_span.get_text(strip=True) if date_span else "Date non trouvée"
        
        # Extraction de la référence et du lien
        item_ref = first_item.find("div", class_="item-ref")
        if item_ref:
            a_tag = item_ref.find("a")
            if a_tag:
                ref_text = a_tag.get_text(strip=True)
                ref_link = a_tag.get("href")
            else:
                ref_text = "Alerte non trouvée"
                ref_link = "Lien non trouvé"
        else:
            ref_text = "Alerte non trouvée"
            ref_link = "Lien non trouvé"
        
        # Affichage des résultats
        print("Date :", date_text)
        print("Référence :", ref_text)
        print("Lien :", ref_link)

else:
    print("Erreur lors de la requête :", response.status_code)
