import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 1) Scraper la page
url = "http://books.toscrape.com/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")

# 2) Mapping des notes
words = ["One", "Two", "Three", "Four", "Five"]
rating_map = {word: i+1 for i, word in enumerate(words)}
books = []

for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]

    price_text = book.select_one(".price_color").text
    price_str = ''.join(c for c in price_text if c.isdigit() or c == '.')
    price = float(price_str)

    rating_class = book.select_one("p.star-rating")["class"][1]
    rating = rating_map[rating_class]

    availability = book.select_one(".availability").text.strip()

    image_relative_url = book.img["src"]
    # Construire l'URL complète sans urljoin
    image_url = url + image_relative_url.replace("../", "")

    books.append({
        "Titre": title,
        "Prix": price,
        "Note": rating,
        "Disponibilité": availability,
        "Image_URL": image_url
    })

# 3) Créer le DataFrame
df = pd.DataFrame(books)
print(df.head())
print("-" * 60)

# 4) Calculs
prix_moyen = round(df["Prix"].mean(), 2)
print("Prix moyen :", prix_moyen)
print("-" * 60)

livre_plus_cher = df.loc[df["Prix"].idxmax()]
print("Livre le plus cher :")
print(livre_plus_cher)
print("-" * 60)

livre_moins_cher = df.loc[df["Prix"].idxmin()]
print("Livre le moins cher :")
print(livre_moins_cher)
print("-" * 60)

repartition_notes = df["Note"].value_counts().sort_index()
print("Répartition par note :")
print(repartition_notes)
print("-" * 60)


# 5) Sauvegarde CSV
df.to_csv("livres.csv", index=False, encoding="utf-8")
print ("Sauvegarge effectuée")
print("-" * 60)
# 6) Fonction pour télécharger l'image
def download_image(image_url, save_path):
    response = requests.get(image_url)
    response.raise_for_status()
    folder = os.path.dirname(save_path)
    if folder: 
        os.makedirs(folder, exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)

image_url = livre_plus_cher["Image_URL"]
save_path = "image.jpg" 

print(f"Téléchargement de l'image du livre le plus cher: {save_path}")
download_image(image_url, save_path)
print("Téléchargement terminé.")
print("-" * 60)
