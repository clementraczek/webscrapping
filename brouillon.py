import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#1
url = "http://books.toscrape.com/"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")


#2
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
    image_url = url + image_relative_url.replace("../", "")

    books.append({
        "Titre": title,
        "Prix": price,
        "Note": rating,
        "Disponibilité": availability,
        "Image_URL": image_url
    })

#3
df = pd.DataFrame(books)
print(df.head())

#4
prix_moyen = round(df["Prix"].mean(), 2)
print("Prix moyen :", prix_moyen)

livre_plus_cher = df.loc[df["Prix"].idxmax()]
print("Livre le plus cher :")
print(livre_plus_cher)

livre_moins_cher = df.loc[df["Prix"].idxmin()]
print("Livre le moins cher :")
print(livre_moins_cher)

repartition_notes = df["Note"].value_counts().sort_index()
print("Répartition par note :")
print(repartition_notes)

#5
df.to_csv("livres.csv", index=False, encoding="utf-8")

#6

image_name = livre_plus_cher["Titre"].replace(" ", "_").replace("/", "_") + ".jpg"
image_path = os.path.join(os.getcwd(), image_name)


img_response = requests.get(livre_plus_cher["Image_URL"])
with open(image_path, "wb") as f:
    f.write(img_response.content)

print(f"Image téléchargée : {image_path}")