# 🏡 Immo Agent – AI Mail Analyzer voor Vastgoed Nieuwsbrieven en Alerts

Deze tool werkt volledig via het automatisch ophalen van nieuwsbrieven en alerts uit je Gmail-inbox, zonder scraping. Dankzij AI-filtering worden alleen de panden getoond die voldoen aan jouw criteria, zodat je snel en efficiënt je ideale woning vindt.

---

## 🛠 Procesflow (functioneel)

1. Gmail filters en labels worden ingesteld om vastgoednieuwsbrieven en alerts automatisch te verzamelen.
2. Het systeem haalt dagelijks de gelabelde e-mails op via de Gmail API.
3. Harde filters worden toegepast op regiozones, prijs, type woning en aantal slaapkamers.
4. AI analyseert de resterende panden, geeft een score en een motivatie voor selectie.
5. Er wordt een dagelijks overzicht gegenereerd in meerdere formaten: Markdown, CSV, Google Sheets en Notion.
6. Rapporten kunnen eenvoudig worden gedeeld of verder verwerkt.

Voor een visuele weergave van deze flow, zie de diagrammen in de documentatiemap.

---

## ✅ Functionaliteit

- Gebruik van Gmail labels en filters om vastgoednieuwsbrieven en alerts automatisch te verzamelen.
- Automatisch ophalen van gelabelde e-mails via de Gmail API.
- Harde filters op:
  - Regiozones
  - Prijs
  - Type woning (huis/appartement)
  - Aantal slaapkamers
- AI-score en motivatie per pand voor betere selectie.
- Dagelijks overzicht in verschillende formaten:
  - Markdown-rapport
  - CSV-bestand
  - Google Sheets integratie
  - Notion integratie

---

## 🔧 Setup

### 1. Virtuele omgeving activeren

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\activate  # Windows
```

Controleer:
```bash
which python  # Moet .venv tonen
```

### 2. Vereisten installeren

```bash
pip install -r requirements.txt
```

### 3. Gmail API configureren

1. Ga naar [Google Cloud Console](https://console.cloud.google.com/).
2. Maak een project aan en activeer de **Gmail API**.
3. Download `credentials.json` en plaats dit in de root van het project.
4. Maak in Gmail filters en labels aan om vastgoednieuwsbrieven en alerts automatisch te herkennen en te labelen (bijv. label `ImmoAgent`).
5. Start de OAuth-flow:

```bash
python scripts/test_gmail.py
```

Dit opent een browser voor toestemming. Daarna wordt `token.pickle` aangemaakt.

### 4. API-sleutels instellen

Maak een `.env` bestand in de root met de volgende variabelen:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-openai-xxxxx
```

Andere API-sleutels kunnen later toegevoegd worden voor extra integraties.

---

## 🚀 Dagelijkse run

Gebruik het hoofdscript om dagelijks het volledige proces te draaien:

```bash
python run_daily_digest.py --zones "Brussel, Antwerpen" --top 10
```

Parameters:

- `--zones`: filter op regiozones (komma-gescheiden lijst).
- `--top`: aantal topresultaten per dag.

Losse scripts in `scripts/` zijn beschikbaar voor debuggen en ontwikkeling, maar het hoofdproces verloopt via `run_daily_digest.py`.

---

## 🗺 Toekomstige uitbreidingen

- Automatische dagelijkse e-maildistributie van de rapporten.
- Feedback-loop voor continue verbetering van AI-selectie.
- Multi-model routering om verschillende AI-modellen te combineren.
- Integraties met Notion, Google Sheets en dashboards voor betere visualisatie en samenwerking.

---

## 👨‍💻 Ontwikkelnotities

- Werkt op macOS en Linux.
- Alle scripts draaien binnen de `.venv` virtuele omgeving.
- Documentatie wordt continu aangevuld tijdens ontwikkeling.
- Focus ligt op gebruiksvriendelijkheid en uitbreidbaarheid.

---

Veel succes met het vinden van je ideale woning! 🏠