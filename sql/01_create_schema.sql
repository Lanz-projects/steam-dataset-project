-- PostgreSQL schema for the Steam Games project.
-- The main table keeps one row per game. Multi-value fields use bridge tables.

BEGIN;

CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.games (
    app_id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    release_date DATE NOT NULL,
    release_year SMALLINT NOT NULL,
    required_age SMALLINT,
    price NUMERIC(10, 2),
    is_free BOOLEAN NOT NULL,
    dlc_count INTEGER,
    discount INTEGER,
    achievements INTEGER,
    recommendations BIGINT,

    user_score SMALLINT,
    user_score_available BOOLEAN,
    user_score_analysis DOUBLE PRECISION,
    metacritic_score SMALLINT,
    metacritic_score_available BOOLEAN,
    metacritic_score_analysis DOUBLE PRECISION,
    score_rank DOUBLE PRECISION,

    positive BIGINT,
    negative BIGINT,
    review_count BIGINT NOT NULL,
    positive_ratio DOUBLE PRECISION,

    estimated_owners TEXT,
    owners_lower BIGINT,
    owners_upper BIGINT,
    owners_midpoint DOUBLE PRECISION,

    peak_ccu INTEGER,
    peak_ccu_available BOOLEAN,
    peak_ccu_analysis DOUBLE PRECISION,

    average_playtime_forever INTEGER,
    average_playtime_forever_available BOOLEAN,
    average_playtime_forever_analysis DOUBLE PRECISION,
    average_playtime_2weeks INTEGER,
    average_playtime_2weeks_available BOOLEAN,
    average_playtime_2weeks_analysis DOUBLE PRECISION,
    median_playtime_forever INTEGER,
    median_playtime_forever_available BOOLEAN,
    median_playtime_forever_analysis DOUBLE PRECISION,
    median_playtime_2weeks INTEGER,
    median_playtime_2weeks_available BOOLEAN,
    median_playtime_2weeks_analysis DOUBLE PRECISION,

    windows BOOLEAN NOT NULL,
    mac BOOLEAN NOT NULL,
    linux BOOLEAN NOT NULL,

    has_metacritic BOOLEAN NOT NULL,
    has_playtime BOOLEAN NOT NULL,

    detailed_description TEXT,
    about_the_game TEXT,
    short_description TEXT,
    reviews TEXT,
    website TEXT,
    support_url TEXT,
    support_email TEXT,
    metacritic_url TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS analytics.game_genres (
    app_id BIGINT NOT NULL REFERENCES analytics.games(app_id) ON DELETE CASCADE,
    genre TEXT NOT NULL,
    PRIMARY KEY (app_id, genre)
);

CREATE TABLE IF NOT EXISTS analytics.game_tags (
    app_id BIGINT NOT NULL REFERENCES analytics.games(app_id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    vote_count INTEGER,
    PRIMARY KEY (app_id, tag)
);

CREATE TABLE IF NOT EXISTS analytics.game_categories (
    app_id BIGINT NOT NULL REFERENCES analytics.games(app_id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    PRIMARY KEY (app_id, category)
);

CREATE TABLE IF NOT EXISTS analytics.game_developers (
    app_id BIGINT NOT NULL REFERENCES analytics.games(app_id) ON DELETE CASCADE,
    developer TEXT NOT NULL,
    PRIMARY KEY (app_id, developer)
);

CREATE TABLE IF NOT EXISTS analytics.game_publishers (
    app_id BIGINT NOT NULL REFERENCES analytics.games(app_id) ON DELETE CASCADE,
    publisher TEXT NOT NULL,
    PRIMARY KEY (app_id, publisher)
);

CREATE INDEX IF NOT EXISTS idx_games_release_year
    ON analytics.games (release_year);

CREATE INDEX IF NOT EXISTS idx_games_is_free
    ON analytics.games (is_free);

CREATE INDEX IF NOT EXISTS idx_games_review_count
    ON analytics.games (review_count);

CREATE INDEX IF NOT EXISTS idx_games_owners_midpoint
    ON analytics.games (owners_midpoint);

CREATE INDEX IF NOT EXISTS idx_game_genres_genre
    ON analytics.game_genres (genre);

CREATE INDEX IF NOT EXISTS idx_game_tags_tag
    ON analytics.game_tags (tag);

CREATE INDEX IF NOT EXISTS idx_game_categories_category
    ON analytics.game_categories (category);

CREATE INDEX IF NOT EXISTS idx_game_developers_developer
    ON analytics.game_developers (developer);

CREATE INDEX IF NOT EXISTS idx_game_publishers_publisher
    ON analytics.game_publishers (publisher);

COMMIT;
