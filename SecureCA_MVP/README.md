# SecureCA MVP — Ready to Run

A small academic prototype demonstrating Client 360°, CSV imports, basic cross-source reconciliation, a review queue, and a regulatory updates screen.

**Important:** Included data is synthetic. Regulatory rows are placeholders, not verified current tax-law updates. Do not use this prototype for real client decisions.

## Run on Windows
1. Install Python 3.10 or newer from https://www.python.org/downloads/ (select “Add Python to PATH”).
2. Extract this ZIP.
3. Open PowerShell or Command Prompt in the extracted `SecureCA_MVP` folder.
4. Run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app should open at http://localhost:8501.

## Files
- `app.py` — application
- `requirements.txt` — dependencies
- `clients.csv` — demo client list
- `accounting_records.csv` — demo accounting entries
- `supporting_records.csv` — demo supporting records
- `tasks.csv` — demo task list
- `regulatory_updates.csv` — placeholder update cards

## CSV columns
- Clients: `client_id`, `client_name`
- Accounting: `client_id`, `reference`, `amount`
- Supporting records: `client_id`, `reference`, `amount`
- Tasks: `client_id`, `task`, `status`
- Regulatory updates: `topic`, `published_date`, `effective_date`, `summary`, `official_source`

## Limitations
CSV imports only; no live software integrations, tax filing, automated tax calculations, automatic legal monitoring, ML, authentication, or production security. Use synthetic/anonymised demo data only.
