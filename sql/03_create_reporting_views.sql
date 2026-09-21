-- Reporting views for Power BI and SQL analysis.
-- Views organize existing tables without copying or changing the data.

BEGIN;

CREATE OR REPLACE VIEW analytics.v_game_summary AS
SELECT
    g.*,
    CASE
        WHEN g.is_free THEN 'Free'
        ELSE 'Paid'
    END AS pricing_type,
    CASE
        WHEN g.is_free THEN 'Free'
        WHEN g.price <= 5 THEN '$0.01-$5'
        WHEN g.price <= 10 THEN '$5-$10'
        WHEN g.price <= 20 THEN '$10-$20'
        WHEN g.price <= 50 THEN '$20-$50'
        ELSE '$50+'
    END AS price_band,
    g.review_count > 0 AS has_reviews,
    ROUND((g.positive_ratio * 100)::numeric, 2) AS positive_percent,
    CASE
        WHEN g.release_date <= CURRENT_DATE THEN 'Released'
        ELSE 'Upcoming'
    END AS release_status,
    (
        SELECT COUNT(*)
        FROM analytics.game_genres gg
        WHERE gg.app_id = g.app_id
    ) AS genre_count,
    (
        SELECT COUNT(*)
        FROM analytics.game_categories gc
        WHERE gc.app_id = g.app_id
    ) AS category_count,
    (
        SELECT COUNT(*)
        FROM analytics.game_tags gt
        WHERE gt.app_id = g.app_id
    ) AS tag_count
FROM analytics.games g;

CREATE OR REPLACE VIEW analytics.v_genre_summary AS
SELECT
    gg.genre,
    COUNT(*) AS game_count,
    COUNT(*) FILTER (WHERE g.review_count > 0) AS reviewed_game_count,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE g.review_count > 0)
        / NULLIF(COUNT(*), 0),
        2
    ) AS pct_with_reviews,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY g.review_count)
        FILTER (WHERE g.review_count > 0) AS median_reviews_when_available,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY g.positive_ratio)
        FILTER (WHERE g.review_count > 0) AS median_positive_ratio,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY g.owners_midpoint)
        FILTER (WHERE g.owners_midpoint > 0) AS median_owners_when_available,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY g.peak_ccu)
        FILTER (WHERE g.peak_ccu > 0) AS median_peak_ccu,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY g.average_playtime_forever)
        FILTER (WHERE g.average_playtime_forever > 0) AS median_playtime,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE g.is_free)
        / NULLIF(COUNT(*), 0),
        2
    ) AS pct_free
FROM analytics.game_genres gg
JOIN analytics.games g ON g.app_id = gg.app_id
WHERE g.release_date <= CURRENT_DATE
GROUP BY gg.genre;

CREATE OR REPLACE VIEW analytics.v_platform_summary AS
WITH historical_games AS (
    SELECT windows, mac, linux
    FROM analytics.games
    WHERE release_date <= CURRENT_DATE
),
platform_counts AS (
    SELECT 'Windows' AS platform, COUNT(*) FILTER (WHERE windows) AS game_count
    FROM historical_games
    UNION ALL
    SELECT 'Mac', COUNT(*) FILTER (WHERE mac)
    FROM historical_games
    UNION ALL
    SELECT 'Linux', COUNT(*) FILTER (WHERE linux)
    FROM historical_games
),
total_games AS (
    SELECT COUNT(*) AS game_count
    FROM historical_games
)
SELECT
    pc.platform,
    pc.game_count,
    ROUND(100.0 * pc.game_count / NULLIF(tg.game_count, 0), 2)
        AS percentage_of_games
FROM platform_counts pc
CROSS JOIN total_games tg;

CREATE OR REPLACE VIEW analytics.v_price_band_summary AS
SELECT
    v.price_band,
    COUNT(*) AS game_count,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE v.review_count > 0)
        / NULLIF(COUNT(*), 0),
        2
    ) AS pct_with_reviews,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY v.review_count)
        FILTER (WHERE v.review_count > 0) AS median_reviews_when_available,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY v.owners_midpoint)
        FILTER (WHERE v.owners_midpoint > 0) AS median_owners_when_available,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY v.peak_ccu)
        FILTER (WHERE v.peak_ccu > 0) AS median_peak_ccu,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY v.average_playtime_forever)
        FILTER (WHERE v.average_playtime_forever > 0) AS median_playtime,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY v.positive_ratio)
        FILTER (WHERE v.review_count > 0) AS median_positive_ratio
FROM analytics.v_game_summary v
WHERE v.release_status = 'Released'
GROUP BY v.price_band;

COMMIT;
