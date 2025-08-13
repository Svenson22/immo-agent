# 🏡 Immo Agent – AI personal analyzer for house and apartment search

This tool works entirely by automatically fetching newsletters and alerts from your Gmail inbox, without scraping. Thanks to AI filtering, only properties that meet your criteria are shown, allowing you to quickly and efficiently find your ideal home.

---

## 🛠 Process Flow (functional)

1. Gmail filters and labels are set up to automatically collect real estate newsletters and alerts.
2. The system retrieves the labeled emails daily via the Gmail API.
3. Hard filters are applied on region zones, price, property type, and number of bedrooms.
4. AI analyzes the remaining properties, provides a score and a motivation for selection.
5. A daily overview is generated in multiple formats: Markdown, CSV, Google Sheets, and Notion.
6. Reports can be easily shared or further processed.

For a visual representation of this flow, see the diagrams in the documentation folder.

---

## ✅ Functionality

- Use of Gmail labels and filters to automatically collect real estate newsletters and alerts.
- Automatic retrieval of labeled emails via the Gmail API.
- Hard filters on:
  - Region zones
  - Price
  - Property type (house/apartment)
  - Number of bedrooms
- AI score and motivation per property for better selection.
- Daily overview in various formats:
  - Markdown report
  - CSV file
  - Google Sheets integration
  - Notion integration

---

## 🔧 Setup

### 1. Activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\activate  # Windows
```

Check:
```bash
which python  # Should show .venv
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Configure Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **Gmail API**.
3. Download `credentials.json` and place it in the root of the project.
4. Create Gmail filters and labels to automatically recognize and label real estate newsletters and alerts (e.g., label `ImmoAgent`).
5. Start the OAuth flow:

```bash
python scripts/test_gmail.py
```

This will open a browser for authorization. Afterwards, `token.pickle` will be created.

### 4. Set API keys

Create a `.env` file in the root with the following variables:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-openai-xxxxx
```

Other API keys can be added later for additional integrations.

---

## 🚀 Daily run

Use the main script to run the full process daily:

```bash
python run_daily_digest.py --zones "Brussels, Antwerp" --top 10
```

Parameters:

- `--zones`: filter by region zones (comma-separated list).
- `--top`: number of top results per day.

Individual scripts in `scripts/` are available for debugging and development, but the main process runs via `run_daily_digest.py`.

---

## 🗺 Future extensions

- Automatic daily email distribution of the reports.
- Feedback loop for continuous improvement of AI selection.
- Multi-model routing to combine different AI models.
- Integrations with Notion, Google Sheets, and dashboards for better visualization and collaboration.

---

## 👨‍💻 Development notes

- Works on macOS and Linux.
- All scripts run within the `.venv` virtual environment.
- Documentation is continuously updated during development.
- Focus is on user-friendliness and extensibility.

---

Good luck finding your ideal home! 🏠