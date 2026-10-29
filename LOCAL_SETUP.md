# SwasthyaGrid: VS Code + localhost setup

## Windows

1. Extract the whole ZIP. In VS Code, open the extracted **project root** where `app.py`, `requirements.txt`, and the `backend` folder are visible together.
2. Open **Terminal → New Terminal** and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_local.py
python -m streamlit run app.py
```

3. Open `http://localhost:8501`. Save the generated administrator password printed by setup.
4. Stop with **Ctrl+C** in the terminal.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry activation. Alternatively, double-click `run_local_windows.bat`.

## macOS / Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_local.py
python -m streamlit run app.py
```

## Optional FastAPI companion

In a second terminal from the same root, activate `.venv` and run `python -m uvicorn api:app --reload --port 8000`. API documentation: `http://localhost:8000/docs`.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'backend'`**: verify `backend/__init__.py` exists next to `app.py`; open the full extracted root (not only `app.py`) and run Streamlit from that root.
- **Missing package**: activate `.venv`, then run `pip install -r requirements.txt`.
- **Admin bootstrap error**: run `python scripts/setup_local.py` and ensure `.env` has both `SG_BOOTSTRAP_ADMIN_EMAIL` and `SG_BOOTSTRAP_ADMIN_PASSWORD` (at least 14 characters).
- **Port busy**: run `python -m streamlit run app.py --server.port 8502`.
- **Maps fail to load**: internet is needed for OpenStreetMap tiles and address lookup.

## AI triage

The app uses local, transparent keyword rules for triage. No Gemini API key or external AI service is required. Suggestions are advisory and require human review.

