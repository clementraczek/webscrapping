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
