"""Apply the reporting views to the local PostgreSQL database."""

from __future__ import annotations

import os
from pathlib import Path

import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
SQL_PATH = PROJECT_ROOT / "sql" / "03_create_reporting_views.sql"


def load_local_env(path: Path) -> None:
    """Load simple KEY=VALUE entries without printing secret values."""

    if not path.exists():
        raise FileNotFoundError(f"Missing environment file: {path}")

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> None:
    load_local_env(ENV_PATH)

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"Missing reporting views SQL file: {SQL_PATH}")

    connection_options = {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }

    sql_text = SQL_PATH.read_text(encoding="utf-8")
    statements = [
        statement.strip()
        for statement in sql_text.split(";")
        if statement.strip()
    ]

    print("Applying reporting views...")

    with psycopg.connect(**connection_options) as connection:
        with connection.cursor() as cursor:
            for statement_number, statement in enumerate(statements, start=1):
                cursor.execute(statement)
                print(f"Statement {statement_number} completed")

    print("Reporting views applied successfully.")


if __name__ == "__main__":
    main()
