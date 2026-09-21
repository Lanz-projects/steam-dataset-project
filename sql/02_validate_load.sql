-- Main table checks
SELECT 'games_row_count' AS check_name, COUNT(*) AS result
FROM analytics.games;

SELECT 'unique_appids' AS check_name, COUNT(DISTINCT app_id) AS result
FROM analytics.games;

SELECT 'duplicate_appids' AS check_name, COUNT(*) AS result
FROM (
    SELECT app_id
    FROM analytics.games
    GROUP BY app_id
    HAVING COUNT(*) > 1
) duplicates;

-- Check for relationship rows without a matching game
SELECT 'orphan_genres' AS table_name, COUNT(*) AS orphan_rows
FROM analytics.game_genres gg
LEFT JOIN analytics.games g ON g.app_id = gg.app_id
WHERE g.app_id IS NULL

UNION ALL

SELECT 'orphan_tags', COUNT(*)
FROM analytics.game_tags gt
LEFT JOIN analytics.games g ON g.app_id = gt.app_id
WHERE g.app_id IS NULL

UNION ALL

SELECT 'orphan_categories', COUNT(*)
FROM analytics.game_categories gc
LEFT JOIN analytics.games g ON g.app_id = gc.app_id
WHERE g.app_id IS NULL

UNION ALL

SELECT 'orphan_developers', COUNT(*)
FROM analytics.game_developers gd
LEFT JOIN analytics.games g ON g.app_id = gd.app_id
WHERE g.app_id IS NULL

UNION ALL

SELECT 'orphan_publishers', COUNT(*)
FROM analytics.game_publishers gp
LEFT JOIN analytics.games g ON g.app_id = gp.app_id
WHERE g.app_id IS NULL;

-- Sample joined results
SELECT
    g.app_id,
    g.name,
    g.release_year,
    g.price,
    g.review_count,
    g.positive_ratio,
    (
        SELECT COUNT(*)
        FROM analytics.game_genres gg
        WHERE gg.app_id = g.app_id
    ) AS genre_count,
    (
        SELECT COUNT(*)
        FROM analytics.game_tags gt
        WHERE gt.app_id = g.app_id
    ) AS tag_count
FROM analytics.games g
WHERE g.review_count > 0
ORDER BY g.review_count DESC
LIMIT 10;
