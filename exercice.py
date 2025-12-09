import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import time
import csv
from pathlib import Path

#exercice 1


URL_BASE = "http://quotes.toscrape.com"
URL_ACCUEIL = URL_BASE + "/"

print(f"Récupération de l'URL : {URL_ACCUEIL}")
reponse = requests.get(URL_ACCUEIL)
print("   Récupération réussie.\n")

#2 
print("Code de statut de la réponse :")
print(f"{reponse.status_code}")

#3     
print(reponse.text[:500])

#4
print(reponse.encoding)

#5
for cle, valeur in reponse.headers.items():
    print(f"{cle} : {valeur}")

#6
URL_ROBOTS = URL_BASE + "/robots.txt"
reponse_robots = requests.get(URL_ROBOTS)
print(reponse_robots.text)

#exerice 2

URL_BASE = "http://quotes.toscrape.com"

#1
headers = {'User-Agent': 'My Scraper 1.0'}
def fetch_page(url, timeout=1):
    """Récupère une page avec gestion d'erreurs."""
    
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout
        )
        # Lève une exception si le code HTTP est 4xx ou 5xx
        response.raise_for_status()
        return response.text


    except Timeout:
        print(f"Timeout pour {url}")
        return None

    except ConnectionError:
        print(f"Erreur de connexion pour {url}")
        return None

    except requests.exceptions.HTTPError:
        # On peut accéder au code HTTP via response.status_code
        print(f"Erreur HTTP {response.status_code}: {url}")
        return None

    except RequestException as e:
        # Regroupe les autres erreurs possibles (ex: URL invalide)
        print(f"Erreur générale: {e}")
        return None

if __name__ == "__main__":

    url_ok = "https://www.wikipedia.org"

    url_invalide = "https://domaine_qui_n_existe_pas_du_tout.xyz"

    print("=== Test avec une URL valide ===")
    html_ok = fetch_page(url_ok)
    if html_ok:
        print("La page valide a bien été récupérée (longueur) :", len(html_ok))

    print("\n=== Test avec une URL invalide ===")
    html_ko = fetch_page(url_invalide)
    if html_ko is None:
        print("Aucune page récupérée, comme prévu.")

#2
pages_html = {}

def scraper():
    print("Scraping en cours...")
    with requests.Session() as session:
        for i in range(1, 4): 
            url = f"{URL_BASE}/page/{i}/"
            print(f"Traitement de la page n°{i} : {url}")

            html = fetch_page(url)

            if html:
                pages_html[i] = html
                print(f"Page {i} récupérée ({len(html)} caractères)")
            else:
                print(f"Échec de récupération de la page {i}")
            time.sleep(1)
scraper()
