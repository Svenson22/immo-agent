import requests
from bs4 import BeautifulSoup
import json
import re

# 🔗 Gebruik hier jouw gewenste Immoweb-link
url = "https://www.immoweb.be/nl/zoekertje/huis/te-koop/sint-kwintens-lennik/1750/20678025"

# 🧠 Headers om te doen alsof we een echte browser zijn
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "nl-BE,nl;q=0.9,en;q=0.8"
}

# 🔄 HTML ophalen
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 🕵️ Zoek de <script> tag met window.classified erin
    script_tag = soup.find("script", string=re.compile("window.classified"))

    if script_tag:
        raw_js = script_tag.string

        # 🎯 Haal het JSON-gedeelte eruit met regex
        match = re.search(r"window\.classified\s*=\s*(\{.*\});", raw_js)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)

            # 🎉 Data extraheren
            title = data.get("property", {}).get("type", "geen type")
            price = data.get("price", {}).get("mainValue", "geen prijs")
            bedrooms = data.get("bedroomCount", "onbekend")
            postal_code = data.get("property", {}).get("location", {}).get("postalCode", "geen postcode")
            street = data.get("property", {}).get("location", {}).get("street", "onbekende straat")
            epc = data.get("energy", {}).get("epcScore", "geen EPC")

            print("🏡 --- Zoekertje ---")
            print(f"🏷️ Type: {title}")
            print(f"💰 Prijs: €{price}")
            print(f"🛏️ Slaapkamers: {bedrooms}")
            print(f"📍 Adres: {street}, {postal_code}")
            print(f"⚡ EPC-score: {epc}")
        else:
            print("⚠️ JSON niet gevonden in script-tag.")
    else:
        print("⚠️ Geen script-tag met 'window.classified' gevonden.")
else:
    print(f"Fout bij ophalen van pagina: {response.status_code}")