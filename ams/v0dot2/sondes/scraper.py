import requests
import json
from bs4 import BeautifulSoup

def get_alerte():
    url = "https://www.cert.ssi.gouv.fr/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Recherche du premier objet correspondant a la liste des alertes
        first_item = soup.find("div", class_="item cert-cti open")

        if first_item:
            # Extraction de la date
            date_span = first_item.find("span", class_="item-date")
            date_text = date_span.get_text(strip=True) if date_span else "Date non trouvée"

            # Extraction de l'alerte et du lien
            alerte_div = first_item.find("div", class_="item-ref")
            if alerte_div:
                a_tag = alerte_div.find("a")
                if a_tag:
                    alerte_text = a_tag.get_text(strip=True)
                    alerte_link = url + a_tag.get("href")
                else:
                    alerte_text = "Alerte non trouvée"
                    alerte_link = "Lien non trouvé"
            else:
                alerte_text = "Alerte non trouvée"
                alerte_link = "Lien non trouvé"

            alerte = {
                "Date": date_text,
                "Alerte": alerte_text,
                "Lien": alerte_link
            }
            
            return alerte
    else:
        print("Erreur lors de la requête :", response.status_code)
        return {"Erreur": f"Erreur HTTP {response.status_code}"}

if __name__ == "__main__":
    # Au lieu d'écrire dans un fichier, on imprime le résultat JSON
    print(json.dumps(get_alerte()))
