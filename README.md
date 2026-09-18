# Steam Games Data Analytics Project

## Project overview

This is an end-to-end data analytics portfolio project using the FronkonGames Steam Games Dataset.

The goal is to understand what the dataset can tell us about Steam games while building practical skills in data cleaning, exploratory analysis, SQL, data modeling, and dashboard design.

This is also a learning project. I want to understand the decisions behind the analysis rather than simply produce charts or a finished dashboard.

## Questions I want to investigate

- How has the Steam game catalog changed by release year?
- Which genres and categories are associated with higher review counts, estimated ownership, or player engagement?
- How does price relate to reviews, estimated ownership, peak concurrent users, and playtime?
- What characteristics are common among highly reviewed games?
- Which games substantially outperform others within their genre or release period?
- How do developers and publishers compare?
- What patterns become visible when looking at tags, categories, and platform support?
- How much of the dataset is missing, zero-filled, or otherwise unreliable?

These questions may change as the data is explored. If the dataset cannot support a question reliably, that limitation should be documented rather than hidden.

## Dataset and source decisions

The dataset is available through the [FronkonGames Steam Games Dataset on Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset).

The JSON file is being used as the main source for the analysis. The CSV export contains shifted or mislabeled columns in part of its header, which can cause values to appear under the wrong field names. The JSON field names and values line up more reliably with the records.

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

The project is designed around this general flow:

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

The analysis will focus on creating useful measures and answering real questions. SQL techniques and statistical methods should support the analysis rather than being included only to demonstrate syntax.

Multi-value fields such as genres, tags, developers, publishers, and categories need special attention because one game can have several values. Tags may also include vote counts, so they may require additional information beyond a simple game-to-tag relationship.

## Interpretation and limitations

- The dataset is a snapshot of the Steam catalog, not a complete history of Steam activity.
- Release-year analysis describes the games in the dataset by release year; it does not measure total yearly Steam revenue or market size.
- Owner counts are estimates rather than exact sales.
- Zero values may mean unavailable data, no recorded activity, a free price, or a valid zero depending on the field.
- Review counts, owner estimates, peak CCU, and playtime are highly skewed by a small number of very popular games.
- Positive review percentages can be misleading for games with very few reviews.
- Correlation will not be treated as proof of causation.
- Missing or incomplete metadata may affect comparisons between games, genres, developers, and publishers.

## What this project is not

This is not intended to be a machine-learning project. The focus is descriptive and exploratory analytics, analytical SQL, data modeling, and communicating findings clearly.

The goal is not to claim that one feature causes a game to succeed. The goal is to identify patterns, explain how the measures were created, and be honest about what the data can and cannot show.
