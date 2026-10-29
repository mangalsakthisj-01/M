"""Prepare a safe local .env for SwasthyaGrid development.

This script only configures local development. It does not create accounts in the
DB until the app starts, and it never overwrites already-populated secrets.
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
TEMPLATE_FILE = ROOT / ".env.example"


def read_env_lines(path: Path) -> tuple[list[str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    values: dict[str, str] = {}
    for line in lines:
        clean = line.strip()
        if not clean or clean.startswith("#") or "=" not in clean:
            continue
        key, value = clean.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return lines, values


def set_env_line(lines: list[str], key: str, value: str) -> list[str]:
    replacement = f"{key}={value}"
    for index, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[index] = replacement
            return lines
    lines.append(replacement)
    return lines


def main() -> None:
    if not ENV_FILE.exists():
        if not TEMPLATE_FILE.exists():
            raise SystemExit("Could not find .env.example. Run this script from the full SwasthyaGrid project.")
        ENV_FILE.write_text(TEMPLATE_FILE.read_text(encoding="utf-8"), encoding="utf-8")
        print("Created .env from .env.example")

    lines, values = read_env_lines(ENV_FILE)
    generated_password = False

    if not values.get("DATABASE_URL"):
        lines = set_env_line(lines, "DATABASE_URL", "sqlite:///./data/swasthyagrid_app.db")
    if not values.get("APP_ENV"):
        lines = set_env_line(lines, "APP_ENV", "development")
    if not values.get("SG_JWT_SECRET"):
        lines = set_env_line(lines, "SG_JWT_SECRET", secrets.token_urlsafe(48))

    admin_email = values.get("SG_BOOTSTRAP_ADMIN_EMAIL", "").strip()
    if not admin_email:
        admin_email = input("Local administrator email [admin@swasthyagrid.local]: ").strip()
        if not admin_email:
            admin_email = "admin@swasthyagrid.local"
        lines = set_env_line(lines, "SG_BOOTSTRAP_ADMIN_EMAIL", admin_email)

    admin_password = values.get("SG_BOOTSTRAP_ADMIN_PASSWORD", "")
    if len(admin_password) < 14:
        admin_password = secrets.token_urlsafe(20)
        generated_password = True
        lines = set_env_line(lines, "SG_BOOTSTRAP_ADMIN_PASSWORD", admin_password)

    if not values.get("SG_BOOTSTRAP_ADMIN_NAME"):
        lines = set_env_line(lines, "SG_BOOTSTRAP_ADMIN_NAME", "SwasthyaGrid Administrator")
    if not values.get("SG_BOOTSTRAP_ADMIN_JURISDICTION"):
        lines = set_env_line(lines, "SG_BOOTSTRAP_ADMIN_JURISDICTION", "Coimbatore, Tamil Nadu")

    ENV_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    if os.name != "nt":
        ENV_FILE.chmod(0o600)

    (ROOT / "data" / "private_uploads").mkdir(parents=True, exist_ok=True)
    (ROOT / "data").mkdir(parents=True, exist_ok=True)

    print("\nLocal configuration is ready.")
    print(f"Administrator email: {admin_email}")
    if generated_password:
        print(f"Generated administrator password (save it now): {admin_password}")
    else:
        print("Administrator password: kept from your existing .env")
    print("Database: SQLite file in ./data (local development only)")
    print("Do not commit .env or use this local database for real citizen/health data.\n")


if __name__ == "__main__":
    main()
