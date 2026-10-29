# Deploy SwasthyaGrid to Streamlit Community Cloud


## 1. Push the complete project to GitHub

1. Extract the ZIP.
2. Create/open a GitHub repository. Upload **all files and folders inside the extracted root**.
3. On GitHub, verify that the repository root contains `app.py`, `requirements.txt`, and `backend/__init__.py` plus the other `backend/*.py` modules.
4. Confirm there is no `.env`, `.streamlit/secrets.toml`, database file, or private upload directory in GitHub.

If using Git locally from the extracted root:

```bash
git init
git add .
git status --short
git commit -m "Deploy SwasthyaGrid Streamlit app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Before committing, inspect `git status` and make sure no credentials or real data are staged.

## 2. Create the Streamlit app

1. Go to https://share.streamlit.io/ and choose **Create app**.
2. Select your repository and branch.
3. Set **Main file path** to `app.py` (not a file inside `src/` and not `api.py`).
4. In **Advanced settings**, choose Python **3.12** for a stable reproducible environment.
5. Deploy.

## 3. Configure secrets

Configure only the database, administrator bootstrap, and security settings required by `.streamlit/secrets.example.toml`. No AI API key is required; triage uses local keyword rules. Never commit real secrets.

## 4. Bootstrap administrator

Set `SG_BOOTSTRAP_ADMIN_EMAIL`, `SG_BOOTSTRAP_ADMIN_PASSWORD` (14+ characters), `SG_BOOTSTRAP_ADMIN_NAME`, and `SG_BOOTSTRAP_ADMIN_JURISDICTION` before first startup. Sign in with that account. Once access is confirmed, remove both `SG_BOOTSTRAP_ADMIN_EMAIL` and `SG_BOOTSTRAP_ADMIN_PASSWORD` from hosting secrets; the existing admin account remains. Never use the local development credentials in a public deployment.

## 5. Test the deployed app

- Register a test citizen and submit a fictional complaint.
- Confirm the citizen can only view their own cases.
- As admin, create Field Officer and Representative accounts, assign a case, and publish a hotspot.
- Confirm jurisdiction-appropriate users receive in-app notifications.
- As field officer, add investigation observations/action/pending work and upload evidence.
- Download CSV and PDF reports.
- Inspect analytics, CivicPulse candidate signals, status history and audit chain.

## Troubleshooting the earlier `No module named 'backend'` error

This error is almost always caused by an incomplete GitHub upload or setting the wrong repository path. The `backend` directory is a required sibling of `app.py`; it must contain `__init__.py`, `ai_triage.py`, `bootstrap.py`, `civicpulse.py`, `database.py`, `mailer.py`, `reports.py`, `security.py`, `security_controls.py`, `services.py`, `storage.py`, and `worker.py`. This package adds a root-path safeguard, but it cannot import files that were not uploaded. Re-upload the full archive contents and redeploy with main file path `app.py`.

## Production caveats

Streamlit is a single-page application host, not a substitute for a full operational deployment. Configure managed database persistence, private object storage for evidence, backups, TLS, least-privilege service credentials, monitoring, retention policy, and a privacy/security review before accepting real citizen data. AI triage is decision support only, not a medical diagnosis or confirmation of an outbreak.
