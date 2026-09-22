# Analysis Summary

## 1. How has the Steam game catalog changed by release year?

The dataset has very few games in the earlier years, but that number increases greatly after 2013. The highest count is 24,976 games in 2025. There are 19,317 games in 2026, but since the year is not over, this does not indicate a decline.

The dataset also includes games released before Steam became available in 2003. Because of this, the earlier records may represent a game's original release rather than when it first appeared on Steam. I would separate those records from the main Steam-era analysis instead of treating them as direct evidence of Steam's catalog growth.

Overall, the later years contain far more games in this dataset, but this reflects the coverage of the dataset rather than the complete history of Steam's market. The pre-2003 records are kept for context, while the main trend should focus on 2003 onward.

## 2. Which genres and categories are associated with higher review activity?

Genres and categories can overlap because a game can have more than one genre or category. I used at least 100 games for genres and at least 500 games for categories so that very small groups would not affect the results too much. The median review counts only include games that had at least one review.

Indie was the most common genre, with 94,379 games. Casual had 59,627 games, Action had 52,651, and Adventure had 51,396. However, the most common genres did not always have the highest median review counts. Massively Multiplayer had the highest median at 73 reviews, followed by Free To Play with 69, Web Publishing with 65, RPG with 36, and Simulation with 33. Among the most common genres, Indie had a median of 23 reviews, Casual had 18, Action had 22, and Adventure had 27.

The category results showed a similar pattern. Remote Play on Tablet had a median of 5,439 reviews, followed by Remote Play on Phone with 2,791, Surround Sound with 2,308.5, Adjustable Text Size with 652, and DualShock Controller Support with 546. These results show an association, but they do not prove that a genre or feature causes a game to receive more reviews.

Overall, the genres and categories with the most games were not always the ones with the highest typical review counts. This part of the analysis mainly uses reviews as a way to measure visibility or engagement. It does not directly compare estimated owners, peak CCU, or playtime by genre or category. Those measures would need to be compared separately because many of their values are zero or unavailable, and a small number of very popular games can affect the results.

## 3. How does price relate to reviews, estimated ownership, peak CCU, and playtime?

There does not seem to be a strong relationship between game price and reviews. Among games with at least one review, the price bands with the highest median review counts were $20–$50, at 97 reviews, and $10–$20, at 59 reviews. The $50+ group had a much lower median of 13 reviews. Free games had a median of 45 reviews, but only 29.72% had reviews, compared with 69.23% of games priced $0.01–$5. So the free-game median describes the free games that had reviews, not all free games. The pattern is mixed, and price alone does not explain how many reviews a game gets.

In the price-band table, median owner estimates were 10,000 in every band when a positive estimate was available. Median peak CCU was highest in the $20–$50 band, at 18, while median playtime increased from 147 minutes for free games to 1,258 minutes for games priced $50+. The $50+ group had 686 games, so its median comes from a much smaller group.

The heatmap, which used Spearman correlations on log-transformed measures, showed weak positive relationships between price and reviews (0.13), estimated owners (0.19), peak CCU (0.20), and playtime (0.23). Overall, price had only a weak relationship with these engagement measures in this dataset. These patterns do not show that price causes a game to receive more reviews, owners, players, or playtime.

## 4. What characteristics are common among highly reviewed games?

The top 5% most-reviewed games generally had higher positive-review percentages, owner estimates, peak CCU, and playtime than other reviewed games. Their median positive-review percentage was 87.92%, compared with 81.25% for other reviewed games. Among games with each measure recorded, the top group also had higher median owner estimates (750,000 compared with 10,000), peak CCU (59 compared with 2), and playtime (679 minutes compared with 186 minutes).

The top group had a slightly larger share of free games (14.86% compared with 9.99%), but most games in both groups were paid. Price type may differ somewhat between the groups, but this comparison does not show that being free causes a game to receive more reviews. Owner counts are estimates, and these results describe patterns in this dataset rather than guarantees about individual games.

## 5. Which games substantially outperform others within their genre or release period?

Several of the same games, including Counter-Strike 2, PUBG: BATTLEGROUNDS, Dota 2, and Terraria, stand out both within their genres and among games released in the same year. In this analysis, a high percentile means that a game has more reviews than most other reviewed games in its group. This does not mean the game is the best; it means that it received more reviews than other games in that group. Review count shows attention or visibility, but it does not measure game quality.

## 6. How do game counts and review activity vary across developers and publishers?

I compared the 20 largest developer groups and the 20 largest publisher groups, then separately looked at organizations with at least 20 reviewed games. The results varied quite a bit. Having more games did not automatically mean having more reviews per game. For example, EroticGamesClub had 239 games in the developer summary, but none had reviews. Choice of Games had 184 games, and 91.85% had reviews, with a median of 20 reviews among those reviewed games.

Publishers showed a similarly mixed pattern. BFG Entertainment had 554 games, with 91.88% having reviews, but the median was 8 reviews per reviewed game. PlayWay S.A. had 295 games; 44.75% had reviews, and the median among those reviewed games was 430. 8floor had 268 games, with 99.25% having reviews, but a median of 8 reviews. So review coverage and the number of reviews per game did not consistently increase with catalog size.

Valve stood out among the developers with at least 20 reviewed games: 35 of its 36 games had reviews, and the median review count was 40,659. That is one notable example, not a pattern shared by developers overall. These comparisons are descriptive, and a game can list multiple developers or publishers, so the counts should not be treated as a simple one-to-one comparison between the two roles.

## 7. What patterns become visible when looking at tags, categories, and platform support?

Windows support was listed for 141,836 games, or 99.96% of the dataset. About 79.19% of games listed Windows support only. Mac and Linux support were less common, appearing on 16.96% and 12.83% of games. This shows which platforms are listed for the games in the dataset, but it does not tell us which operating systems players use.

Single-player was the most common category, listed for 126,372 games (89.06%). Family Sharing appeared on 113,776 games (80.18%), while Steam Achievements appeared on 66,074 (46.56%). These categories can overlap, so a game may have more than one of them.

Indie was the most common genre, with 94,379 games, followed by Casual with 59,627, Action with 52,651, and Adventure with 51,396. Among games with tags, the most common were Singleplayer (50,369), Indie (48,568), Action (36,825), Casual (36,570), and Adventure (35,213).

Overall, the dataset is mostly made up of games that list Windows support, and single-player is a common category. These counts describe how games are labeled; they do not explain why developers chose those features or what players prefer. Tags are missing for 41.24% of games, and games can have several tags, genres, and categories, so those counts overlap and do not add up to the total number of games.

## 8. How much of the dataset is missing, zero-filled, or otherwise unreliable?

Overall, the dataset is useful for looking at many parts of the Steam catalog, but not every column has complete information. The AppIDs were unique, and the release dates and owner ranges passed the checks I ran. Some information is still missing or recorded as zero. For example, 58.48% of games had at least one recorded review, while Metacritic and user scores were zero for 96.99% and 99.97% of games.

The written `reviews` field is blank for 91.12% of games, but that is separate from the positive and negative review counts. A zero can mean different things depending on the column: a price of zero means the game is free, while a zero review count means no positive or negative reviews were recorded. For other columns, zero may mean information was not available, so I need to check what it means before using it.

Overall, the dataset can answer some questions well, but not every column is useful for every comparison. I need to check whether missing or zero values are meaningful before using a field. The checks I ran help catch certain problems, but they do not guarantee that every value in the original dataset is correct.
