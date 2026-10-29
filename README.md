# SwasthyaGrid — Civic Intelligence & Health-Risk Triage

SwasthyaGrid is a civic case-management application with four role-specific dashboards, an OpenStreetMap-powered interactive map, jurisdiction-scoped complaints, administrator-managed hotspots, citizen notifications, field investigation reports, PDF/CSV exports, local rule-based evidence triage, CivicPulse clustering, SLA reminders, cross-department dependencies, and a hash-linked audit trail.

## Deployment package

This archive is **Streamlit-first**. The application entrypoint is `app.py`; required Python service modules are in the sibling `backend/` package. The legacy React/Vite client has deliberately been excluded to avoid having a second, disconnected frontend with a different key-handling path.

- `app.py`: Streamlit UI and role dashboards
- `backend/`: database, auth/security, case workflow, AI triage, map analytics, notifications, reports and storage services
- `api.py`: optional FastAPI companion API
- `requirements.txt`: Python dependencies
- `.streamlit/secrets.example.toml`: safe placeholder template (not active secrets)
- `STREAMLIT_CLOUD_DEPLOY.md`: exact GitHub and Streamlit Cloud deployment steps
- `LOCAL_SETUP.md`: VS Code and localhost setup
- `scripts/setup_local.py`: generates local config and a one-time admin password
- `tests/`: service and API tests

## Run locally in VS Code

Python 3.12 is recommended. From the extracted project root:

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_local.py
python -m streamlit run app.py
```

Open `http://localhost:8501`. The setup helper creates a local `.env` and prints the bootstrap administrator password. Do not commit `.env` or use local SQLite/private uploads for production citizen data.

Optional companion API in another terminal:

```bash
python -m uvicorn api:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`.

## Local triage engine

Triage uses transparent local keyword rules. It makes no external AI calls and requires no Gemini API key or other AI credentials. Suggestions always require human review and are not medical diagnoses or proof of outbreaks. Uploaded images are not interpreted by this rule engine.

## Streamlit Community Cloud

1. Upload the complete extracted root to GitHub. Verify the repository root has both `app.py` and `backend/__init__.py` plus all `backend/*.py` modules.
2. In https://share.streamlit.io/, create an app and use main file path `app.py`. Select Python 3.12 in Advanced settings.
3. Configure secrets from `.streamlit/secrets.example.toml`; use a secure random `SG_JWT_SECRET` and unique admin password. No AI API key is required.
4. For persistent records, use managed PostgreSQL with TLS and backups. Community Cloud local files are not durable. Configure a private object store for evidence in a production pilot.

Detailed instructions, smoke tests, and troubleshooting for the earlier `ModuleNotFoundError: No module named 'backend'` are in [`STREAMLIT_CLOUD_DEPLOY.md`](STREAMLIT_CLOUD_DEPLOY.md).

## Safety and operational boundaries

- Citizen, field officer, administrator and representative views are controlled by application role/jurisdiction checks.
- Hotspots are published by authorized administrators and trigger in-app notifications for affected jurisdictions.
- Field investigation reports track observations, action taken, pending work, evidence and follow-up recommendations.
- CivicPulse clusters are candidates for human review, not confirmed disease outbreaks.
- Local triage suggestions are not diagnoses, proof of authenticity, or a reason to reject a complaint without human review.
- Before real deployment, configure persistent storage, private evidence storage, TLS, backups, monitoring, data-retention rules and security/privacy review.

## Tests

Run from the project root after installing requirements:

```bash
python -m compileall -q app.py api.py backend scripts tests
python -m pytest -q
```

Tests validate backend and API behavior; a live hosted smoke test, managed PostgreSQL/PostGIS, private S3 storage and SMTP must be checked in the target deployment.
