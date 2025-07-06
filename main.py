print("Immo-agent gestart")

import requests
from bs4 import BeautifulSoup

url = "https://www.immoweb.be/nl/zoekertje/nieuwbouwproject-huizen/te-koop/zottegem/9620/20867659"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Titel
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Geen titel gevonden"

    # Prijs
    price_tag = soup.find("p", class_="classified__price")
    price = price_tag.get_text(strip=True) if price_tag else "Geen prijs gevonden"

    print(f"Titel: {title}")
    print(f"Prijs: {price}")
else:
    print(f"Fout bij ophalen van pagina: {response.status_code}")