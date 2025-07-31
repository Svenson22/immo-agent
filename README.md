# 🏡 Immo Agent – AI Mail Analyzer voor Vastgoed

Deze tool verzamelt automatisch e-mails van vastgoedwebsites (zoals Immoweb, Zimmo, Immoscoop) en analyseert deze met AI om enkel de panden te tonen die voldoen aan jouw criteria. Geen scraping nodig – we werken volledig via e-mailintegratie en AI-filtering.

---

## ✅ Functionaliteit

- Haal automatisch e-mails op uit een Gmail-inbox via de **Gmail API**.
- Analyseer inhoud met **Claude (Anthropic) via LangChain**.
- Filter panden op:
  - Regiozones
  - Budget
  - Type (huis/appartement)
- Genereer een dagelijks rapport in **Markdown**.

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
4. Start de OAuth-flow:

```bash
python email_pipeline/gmail_auth.py
```

Dit opent een browser voor toestemming. Daarna wordt `token.pickle` aangemaakt.

### 4. API-sleutels instellen

Maak een `.env` bestand in de root:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

---

## 🚀 Scripts

### 1. E-mails ophalen

Haalt de laatste e-mails op die voldoen aan een query (bv. "subject:immoweb"):

```bash
python email_pipeline/fetch_emails.py
```

### 2. Analyse met AI

Laat Claude via LangChain e-mails scannen op jouw criteria:

```bash
python email_pipeline/analyze_emails.py
```

### 3. Rapport genereren

Genereert een Markdown-rapport met alle matches:

```bash
python email_pipeline/generate_report.py
```

Output:
```
reports/daily_2025-07-31.md
```

---

## 🗺 Toekomstige uitbreidingen

- Automatische dagelijkse mail met resultaten
- Feedback-loop voor betere AI-selectie
- Extra integraties (Notion, Confluence, dashboards)

---

## 👨‍💻 Ontwikkelnotities

- Werkt op macOS
- Alle scripts draaien binnen `.venv`
- Documentatie wordt continu aangevuld tijdens ontwikkeling

---

Veel succes met het vinden van je ideale woning! 🏠