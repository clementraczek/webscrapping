
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"Erreur lors de la requête de {url} : {e}")
        return None

def scrape_quotes(soup):
    quotes_data = []
    for quote in soup.select("div.quote"):
        text = quote.select_one("span.text").get_text(strip=True)
        author = quote.select_one("small.author").get_text(strip=True)
        author_url = quote.select_one("a")["href"]
        tags = [tag.get_text(strip=True) for tag in quote.select("div.tags a.tag")]
        quotes_data.append({
            "Texte": text,
            "Auteur": author,
            "Auteur_URL": f"http://quotes.toscrape.com{author_url}",
            "Tags": tags
        })
    return quotes_data

def get_next_page(soup):
    next_btn = soup.select_one("li.next a")
    if next_btn:
        return f"http://quotes.toscrape.com{next_btn['href']}"
    return None

def scrape_all_quotes(max_pages=10, delay=1):
    url = "http://quotes.toscrape.com"
    all_quotes = []
    page_count = 0

    while url and page_count < max_pages:
        print(f"Scraping page {page_count+1}: {url}")
    
        soup = get_soup(url)
        if soup is None:
            break
        quotes = scrape_quotes(soup)
        all_quotes.extend(quotes)
        url = get_next_page(soup)
        page_count += 1
        time.sleep(delay)
   
    print("-" * 60)
    print(f"Total de citations collectées : {len(all_quotes)}")
    return all_quotes

def process_data(quotes):
    df_citations = pd.DataFrame(quotes)
    authors_dict = {}
    for author in df_citations['Auteur']:
        authors_dict[author] = authors_dict.get(author, 0) + 1
    authors_count = pd.DataFrame(list(authors_dict.items()), columns=['Auteur', 'Nb_Citations'])
    authors_count = authors_count.sort_values(by='Nb_Citations', ascending=False)

    tags_dict = {}
    for tags_list in df_citations['Tags']:
        for tag in tags_list:
            tags_dict[tag] = tags_dict.get(tag, 0) + 1
    tags_count = pd.DataFrame(list(tags_dict.items()), columns=['Tag', 'Frequence'])
    tags_count = tags_count.sort_values(by='Frequence', ascending=False)

    return df_citations, authors_count, tags_count

def generate_statistics(df_citations, authors_count, tags_count):
    print("-" * 60)
    print("Top 5 auteurs les plus cités :")
    print(authors_count.head(5))
    print("-" * 60)
    print("Top 10 tags les plus utilisés :")
    print(tags_count.head(10))
    avg_length = df_citations['Texte'].apply(len).mean()
    print("-" * 60)
    print(f"Longueur moyenne des citations : {avg_length:.2f} caractères")

def main():
    quotes = scrape_all_quotes(max_pages=10, delay=1)
    df_citations, authors_count, tags_count = process_data(quotes)

    with pd.ExcelWriter("quotes.xlsx", engine="xlsxwriter") as writer:
        df_citations.to_excel(writer, sheet_name="Citations", index=False)
        authors_count.to_excel(writer, sheet_name="Auteurs", index=False)
        tags_count.to_excel(writer, sheet_name="Tags", index=False)

    generate_statistics(df_citations, authors_count, tags_count)
    print("-" * 60)
    print("Fichier Excel généré")

if __name__ == "__main__":
    main()
