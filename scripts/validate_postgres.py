"""Run the read-only PostgreSQL validation queries from VS Code."""

from __future__ import annotations

import os
from pathlib import Path

import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
SQL_PATH = PROJECT_ROOT / "sql" / "02_validate_load.sql"


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


def print_result(cursor: psycopg.Cursor, query_number: int) -> None:
    """Print the result of one validation query in a readable format."""

    if cursor.description is None:
        print(f"Query {query_number}: completed")
        return

    column_names = [column.name for column in cursor.description]
    rows = cursor.fetchall()

    print(f"\nQuery {query_number}")
    print(" | ".join(column_names))
    print("-" * 80)

    for row in rows:
        values = ["" if value is None else str(value) for value in row]
        print(" | ".join(values))


def main() -> None:
    load_local_env(ENV_PATH)

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"Missing validation SQL file: {SQL_PATH}")

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

    print("Running PostgreSQL validation checks...")

    with psycopg.connect(**connection_options) as connection:
        with connection.cursor() as cursor:
            for query_number, statement in enumerate(statements, start=1):
                cursor.execute(statement)
                print_result(cursor, query_number)

    print("\nValidation complete.")


if __name__ == "__main__":
    main()
