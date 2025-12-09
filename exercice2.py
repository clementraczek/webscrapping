import requests
from bs4 import BeautifulSoup
import json


#1 
url = "http://quotes.toscrape.com"
response = requests.get(url)

#2

if response.status_code != 200:
    print("Erreur lors du chargement de la page")
    exit()

#3
soup = BeautifulSoup(response.text, "html.parser")

#4
quotes_elements = soup.find_all("div", class_="quote")
print(f"Nombre de citations trouvées : {len(quotes_elements)}")

#5
quotes = []
for quote in quotes_elements:
    text = quote.find("span", class_="text").get_text()
    author = quote.find("small", class_="author").get_text()
    tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
    
    quotes.append({
        "text": text,
        "author": author,
        "tags": tags
    })

#6
print("5 premières citations:")
for q in quotes[:5]:
    print(f"Texte : {q['text']}")
    print(f"Auteur : {q['author']}")
    print(f"Tags : {', '.join(q['tags'])}")
    print("=" * 50)

#7
print(f"Nombre total de citations sur la page : {len(quotes)}")

#8
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=4)

print("Les données ont été sauvegardées dans quotes.json")


#bonus

current_url = url
all_quotes = []  

pages_to_scrape = 4  

for page in range(pages_to_scrape):
    print(f"Scraping page {page + 1}: {current_url}")
    response = requests.get(current_url)
    if response.status_code != 200:
        print(f"Erreur lors du chargement de {current_url}")
        break
    
    soup = BeautifulSoup(response.text, "html.parser")
    quotes_elements = soup.find_all("div", class_="quote")
    
    for quote in quotes_elements:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
        all_quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })
    
    next_btn = soup.find("li", class_="next")
    if next_btn and next_btn.find("a"):
        next_link = next_btn.find("a")["href"]
        current_url = url + next_link
    else:
        print("Pas de page suivante trouvée.")
        break


with open("quotes_multiple_pages.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=4)

print("Les citations ont été sauvegardées dans 'quotes_multiple_pages.json'.")