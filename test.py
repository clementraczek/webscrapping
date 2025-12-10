import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def generate_fridays(start_year):
    """Génère toutes les vendredis depuis start_year jusqu'à aujourd'hui."""
    dt = datetime(start_year, 1, 1)
    today = datetime.today()
    # Avancer jusqu'au premier vendredi
    while dt.weekday() != 4:
        dt += timedelta(days=1)
    while dt <= today:
        yield dt
        dt += timedelta(days=7)

def scrape_atp_ranking(date):
    """Scrape le classement ATP pour une date donnée."""
    url_date = date.strftime("%Y-%m-%d")
    url = f"https://fr.tennistemple.com/classement-atp/{url_date}"
    print(f"Scraping {url} ...")
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Aucun classement disponible pour {url}")
        return None
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("table", {"class": "classement-atp"})
    if not table:
        print(f"Aucun tableau trouvé pour {url}")
        return None
    
    headers = [th.text.strip() for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cols = [td.text.strip() for td in tr.find_all("td")]
        if cols:
            rows.append(cols)
    
    df = pd.DataFrame(rows, columns=headers)
    df['Date'] = date.strftime("%Y-%m-%d")
    return df

def main():
    start_year = 2000  # ou l'année de ton choix
    all_data = []
    for friday in generate_fridays(start_year):
        df = scrape_atp_ranking(friday)
        if df is not None:
            all_data.append(df)
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("classement_atp_historique.csv", index=False, encoding="utf-8-sig")
        print("Classement historique enregistré dans classement_atp_historique.csv")
    else:
        print("Aucune donnée récupérée.")

if __name__ == "__main__":
    main()
