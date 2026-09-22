# Steam Games Data Analytics Project

## Project overview

This is an end-to-end data analytics portfolio project using the FronkonGames Steam Games Dataset.

The goal is to understand what the dataset can tell us about Steam games while building practical skills in data cleaning, exploratory analysis, SQL, data modeling, and dashboard design.

This is also a learning project. I want to understand the decisions behind the analysis rather than simply produce charts or a finished dashboard.

## Questions explored in this project

- How has the Steam game catalog changed by release year?
- Which genres and categories are associated with higher review counts, estimated ownership, or player engagement?
- How does price relate to reviews, estimated ownership, peak concurrent users, and playtime?
- What characteristics are common among highly reviewed games?
- Which games substantially outperform others within their genre or release period?
- How do game counts and review activity vary across developers and publishers?
- What patterns become visible when looking at tags, categories, and platform support?
- How much of the dataset is missing, zero-filled, or otherwise unreliable?

These questions were a starting point and changed as I explored the data. When the dataset could not support a question reliably, I documented that limitation rather than hiding it.

## Dataset and source decisions

The dataset is available through the [FronkonGames Steam Games Dataset on Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset).

I used the JSON file as the main source for the analysis. The CSV export contains shifted or mislabeled columns in part of its header, which can cause values to appear under the wrong field names. The JSON field names and values line up more reliably with the records.

The dataset includes information such as:

- Game names and AppIDs
- Release dates
- Prices and discounts
- Estimated owner ranges
- Peak concurrent users
- Positive and negative reviews
- Playtime
- Developers and publishers
- Genres, categories, and tags
- Platform support

Steam owner counts are estimates and are provided as ranges. They should not be treated as exact sales figures. If a midpoint is calculated from a range, it will be treated only as a rough comparison value.

## Analytical approach

I followed this general flow:

```text
Raw Steam JSON
→ Python and pandas exploration
→ Data cleaning and transformation
→ PostgreSQL analytical model
→ SQL analysis
→ Python analysis and visualization
→ Power BI dashboard
→ Documented findings
```

The analysis focused on creating useful measures and answering questions. SQL and statistical methods supported the analysis rather than being included just to demonstrate syntax.

I handled multi-value fields such as genres, tags, developers, publishers, and categories carefully because one game can have several values. Tags can also include vote counts, so I kept those counts with their tags in the PostgreSQL model.

## Interpretation and limitations

- The dataset is a snapshot of the Steam catalog, not a complete history of Steam activity.
- Release-year analysis describes the games in the dataset by release year; it does not measure total yearly Steam revenue or market size.
- Owner counts are estimates rather than exact sales.
- Zero values may mean unavailable data, no recorded activity, a free price, or a valid zero depending on the field.
- Review counts, owner estimates, peak CCU, and playtime are highly skewed by a small number of very popular games.
- Positive review percentages can be misleading for games with very few reviews.
- Correlation is not proof of causation.
- Missing or incomplete metadata may affect comparisons between games, genres, developers, and publishers.

## What this project is not

This is not intended to be a machine-learning project. The focus is descriptive and exploratory analytics, analytical SQL, data modeling, and communicating findings clearly.

The goal is not to claim that one feature causes a game to succeed. The goal is to identify patterns, explain how the measures were created, and be honest about what the data can and cannot show.

## Conclusion

This project helped me explore what the Steam games dataset can show and learn that the numbers need context. The dataset has 141,900 games. The number of games by release year increases a lot in the later years and reaches its highest point in 2025, with 24,976 games. The 2026 count is from an incomplete year, and the dataset also includes games released before Steam was available, so it does not give a complete history of Steam's catalog.

Some patterns were clearer than others. Indie was the most common genre, but its median review count was 23, compared with 73 for Massively Multiplayer and 69 for Free To Play. Price had only weak relationships with reviews, estimated owners, peak CCU, and playtime. The top 5% most-reviewed games also had higher median positive-review percentages (87.92% compared with 81.25%) and, where values were available, higher median owner estimates (750,000 compared with 10,000), peak CCU (59 compared with 2), and playtime (679 compared with 186 minutes). These patterns do not show that one measure caused another, and review count does not prove a game is better. The developer and publisher results varied, without one clear pattern linking catalog size to review activity.

The AppIDs were unique with none missing, and my checks found no invalid release dates or owner ranges. However, the amount of information varies by column: for example, tags are missing for 41.24% of games, and the written `reviews` field is blank for 91.12%. Zero values also mean different things depending on the column, and owner counts are estimates. Overall, these findings describe this dataset, not the entire Steam market, and they do not explain what caused the patterns.
