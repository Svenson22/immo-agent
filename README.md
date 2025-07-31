# 🏡 Immo Agent – Automatische scraper voor Immoweb

Deze tool verzamelt automatisch links naar huizen en appartementen op Immoweb.be op basis van dynamische regiozones. De gevonden zoekertjes kunnen vervolgens door een AI-module beoordeeld worden op relevantie.

---

## 🔧 Setup

### 1. Virtuele omgeving instellen

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows
```

### 2. Vereisten installeren

```bash
pip install -r requirements.txt
```

### 3. Playwright installeren

```bash
playwright install
```

### 4. CSV-bestanden toevoegen

Plaats het bestand `Conversion_Postal_code_Refnis_code_va01012025.csv` in de hoofdmap van je project. Dit bestand bevat de mapping van gemeentenaam naar postcode.
Je kunt dit downloaden via de officiële site van Statbel:
👉 https://statbel.fgov.be/nl/over-statbel/methodologie/classificaties/geografie

---

## 🚀 Scripts

### 1. `gemeente_to_postcode.py`

Zet gemeentenaam om naar postcode(s) op basis van de conversie-CSV.

**Gebruik:**
```bash
python gemeente_to_postcode.py
```

**Output voorbeeld:**
```bash
['9450', '9420', '1785']
```

### 2. `scrape_links_per_zone.py`

Scrapet Immoweb-links per dynamische zone (bv. Zone 1, Zone 2...) op basis van een `zones.json`-bestand.

**Gebruik:**
```bash
python scrape_links_per_zone.py
```

Zorg dat `zones.json` aanwezig is en de structuur volgt zoals hieronder:
```json
{
  "Zone 1 – Aalst-Haaltert": ["Haaltert", "Erpe-Mere", "Denderleeuw", "Liedekerke"],
  "Zone 2 – Aarschot-Diest": ["Bekkevoort", "Scherpenheuvel-Zichem", "Testelt", "Zelem"],
  "Zone 3 – Opwijk-Merchtem": ["Asse", "Opwijk", "Merchtem", "Wolvertem"]
}
```

De postcodes worden opgevraagd via `gemeente_to_postcode.py` en automatisch in de Immoweb-URL geplaatst in dit formaat:
```
https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&postalCodes=BE-9450,BE-9420
```

---

## 🧪 Testen

Test de postcodeconversie los via:
```bash
python gemeente_to_postcode.py
```

Je kunt daar testgemeenten toevoegen in de `__main__` sectie:
```python
test_gemeenten = ["Haaltert", "Erpe-Mere", "Merchtem", "Lennik"]
```

---

## 🗺 Toekomst

- Scraping uitbreiden met extra filters (prijs, oppervlakte, aantal slaapkamers)
- AI-module toevoegen die inschat of een zoekertje relevant is
- Zones intekenen op kaart via GeoPandas
- Automatische dagelijkse mailing of dashboard

---

## 👨‍💻 Ontwikkelnotities

- Werkt op macOS
- Uitvoering gebeurt in virtuele omgeving via:
```bash
source venv/bin/activate
```
- Playwright wordt gebruikt voor scraping in headless Chromium
- Documentatie wordt continu mee opgebouwd

---

Veel succes met het zoeken naar je ideale woonst! 🏠