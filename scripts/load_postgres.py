"""Load the cleaned Steam dataset into the local PostgreSQL container."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import psycopg
from psycopg import sql


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "steam_games_clean.parquet"
ENV_PATH = PROJECT_ROOT / ".env"

GAME_COLUMN_MAP = {
    "AppID": "app_id",
    "name": "name",
    "release_date": "release_date",
    "release_year": "release_year",
    "required_age": "required_age",
    "price": "price",
    "is_free": "is_free",
    "dlc_count": "dlc_count",
    "discount": "discount",
    "achievements": "achievements",
    "recommendations": "recommendations",
    "user_score": "user_score",
    "user_score_available": "user_score_available",
    "user_score_analysis": "user_score_analysis",
    "metacritic_score": "metacritic_score",
    "metacritic_score_available": "metacritic_score_available",
    "metacritic_score_analysis": "metacritic_score_analysis",
    "score_rank": "score_rank",
    "positive": "positive",
    "negative": "negative",
    "review_count": "review_count",
    "positive_ratio": "positive_ratio",
    "estimated_owners": "estimated_owners",
    "owners_lower": "owners_lower",
    "owners_upper": "owners_upper",
    "owners_midpoint": "owners_midpoint",
    "peak_ccu": "peak_ccu",
    "peak_ccu_available": "peak_ccu_available",
    "peak_ccu_analysis": "peak_ccu_analysis",
    "average_playtime_forever": "average_playtime_forever",
    "average_playtime_forever_available": "average_playtime_forever_available",
    "average_playtime_forever_analysis": "average_playtime_forever_analysis",
    "average_playtime_2weeks": "average_playtime_2weeks",
    "average_playtime_2weeks_available": "average_playtime_2weeks_available",
    "average_playtime_2weeks_analysis": "average_playtime_2weeks_analysis",
    "median_playtime_forever": "median_playtime_forever",
    "median_playtime_forever_available": "median_playtime_forever_available",
    "median_playtime_forever_analysis": "median_playtime_forever_analysis",
    "median_playtime_2weeks": "median_playtime_2weeks",
    "median_playtime_2weeks_available": "median_playtime_2weeks_available",
    "median_playtime_2weeks_analysis": "median_playtime_2weeks_analysis",
    "windows": "windows",
    "mac": "mac",
    "linux": "linux",
    "has_metacritic": "has_metacritic",
    "has_playtime": "has_playtime",
    "detailed_description": "detailed_description",
    "about_the_game": "about_the_game",
    "short_description": "short_description",
    "reviews": "reviews",
    "website": "website",
    "support_url": "support_url",
    "support_email": "support_email",
    "metacritic_url": "metacritic_url",
    "notes": "notes",
}

BRIDGE_TABLES = {
    "genres": ("game_genres", "genre"),
    "categories": ("game_categories", "category"),
    "developers": ("game_developers", "developer"),
    "publishers": ("game_publishers", "publisher"),
}


def load_local_env(path: Path) -> None:
    """Load simple KEY=VALUE entries without printing any secret values."""

    if not path.exists():
        raise FileNotFoundError(f"Missing environment file: {path}")

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def scalar_value(value: Any) -> Any:
    """Convert pandas and NumPy scalar values into database-friendly values."""

    if value is None or value is pd.NA:
        return None

    if isinstance(value, pd.Timestamp):
        return value.date()

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if hasattr(value, "item"):
        return value.item()

    return value


def parse_nested(value: Any, column: str, app_id: Any) -> Any:
    """Restore a nested list or dictionary saved as JSON text."""

    if value is None or value is pd.NA:
        return None

    if isinstance(value, str):
        if not value.strip():
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Could not parse {column} for AppID {app_id}"
            ) from error

    if isinstance(value, (list, dict)):
        return value

    return None


def unique_values(values: Iterable[Any]) -> list[str]:
    """Return non-empty nested values once while preserving their order."""

    result: list[str] = []
    seen: set[str] = set()

    for value in values or []:
        if value is None:
            continue

        cleaned = str(value).strip()
        if cleaned and cleaned not in seen:
            result.append(cleaned)
            seen.add(cleaned)

    return result


def copy_rows(
    connection: psycopg.Connection,
    table_name: str,
    column_names: list[str],
    rows: Iterable[tuple[Any, ...]],
) -> None:
    """Bulk-load rows with PostgreSQL COPY."""

    columns = sql.SQL(", ").join(
        sql.Identifier(column) for column in column_names
    )
    statement = sql.SQL(
        "COPY analytics.{table} ({columns}) FROM STDIN"
    ).format(
        table=sql.Identifier(table_name),
        columns=columns,
    )

    with connection.cursor() as cursor:
        with cursor.copy(statement) as copy:
            for row in rows:
                copy.write_row(row)


def game_rows(data: pd.DataFrame) -> Iterable[tuple[Any, ...]]:
    """Yield rows for the one-row-per-game table."""

    source_columns = list(GAME_COLUMN_MAP)

    for row in data[source_columns].itertuples(index=False, name=None):
        yield tuple(scalar_value(value) for value in row)


def list_bridge_rows(
    data: pd.DataFrame,
    source_column: str,
    value_column: str,
) -> Iterable[tuple[Any, str]]:
    """Yield AppID/value rows for list-based relationship tables."""

    for app_id, raw_value in data[["AppID", source_column]].itertuples(
        index=False,
        name=None,
    ):
        values = parse_nested(raw_value, source_column, app_id)
        for value in unique_values(values):
            yield scalar_value(app_id), value


def tag_rows(data: pd.DataFrame) -> Iterable[tuple[Any, str, Any]]:
    """Yield AppID/tag/vote rows for the tag relationship table."""

    for app_id, raw_tags in data[["AppID", "tags"]].itertuples(
        index=False,
        name=None,
    ):
        tags = parse_nested(raw_tags, "tags", app_id)
        if not isinstance(tags, dict):
            continue

        for tag, vote_count in tags.items():
            cleaned_tag = str(tag).strip()
            if cleaned_tag:
                yield (
                    scalar_value(app_id),
                    cleaned_tag,
                    scalar_value(vote_count),
                )


def reset_tables(connection: psycopg.Connection) -> None:
    """Clear project tables only when the user explicitly requests it."""

    table_names = [
        "game_tags",
        "game_genres",
        "game_categories",
        "game_developers",
        "game_publishers",
        "games",
    ]
    tables = sql.SQL(", ").join(
        sql.SQL("analytics.{}".format(table)) for table in table_names
    )

    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("TRUNCATE TABLE {} CASCADE").format(tables))


def verify_counts(connection: psycopg.Connection) -> None:
    """Print database row counts after the load completes."""

    table_names = [
        "games",
        "game_genres",
        "game_tags",
        "game_categories",
        "game_developers",
        "game_publishers",
    ]

    with connection.cursor() as cursor:
        for table_name in table_names:
            cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM analytics.{}").format(
                    sql.Identifier(table_name)
                )
            )
            count = cursor.fetchone()[0]
            print(f"{table_name}: {count:,} rows")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load the cleaned Steam Parquet file into PostgreSQL."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing project tables before loading.",
    )
    args = parser.parse_args()

    load_local_env(ENV_PATH)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing cleaned dataset: {DATA_PATH}")

    data = pd.read_parquet(DATA_PATH)
    data = data.rename(columns=GAME_COLUMN_MAP)

    connection_options = {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }

    print(f"Loaded source data: {len(data):,} rows")

    with psycopg.connect(**connection_options) as connection:
        if args.reset:
            print("Resetting existing analytics tables...")
            reset_tables(connection)

        copy_rows(
            connection,
            "games",
            list(GAME_COLUMN_MAP.values()),
            game_rows(data.rename(columns={"app_id": "AppID"})),
        )

        for source_column, (table_name, value_column) in BRIDGE_TABLES.items():
            copy_rows(
                connection,
                table_name,
                ["app_id", value_column],
                list_bridge_rows(data.rename(columns={"app_id": "AppID"}), source_column, value_column),
            )

        copy_rows(
            connection,
            "game_tags",
            ["app_id", "tag", "vote_count"],
            tag_rows(data.rename(columns={"app_id": "AppID"})),
        )

        verify_counts(connection)


if __name__ == "__main__":
    main()
