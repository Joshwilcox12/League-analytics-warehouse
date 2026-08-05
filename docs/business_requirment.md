# League Analytics Warehouse

## Business Problem

League of Legends players have access to their match history but struggle to turn that data into actionable insights that help them improve and climb the ranked ladder.

## Goal

Build a data platform that ingests Riot API data and provides meaningful insights to help players improve their gameplay through historical match analysis.

---

# Target User

League of Legends players who want to improve their gameplay using data.

---

# User Stories

As a player,

- I want to view my recent match history so I can quickly review my recent games.
- I want to identify my strongest champions so I know which champions I should play in ranked.
- I want to track whether my gameplay is improving over time.
- I want to understand which champion matchups I struggle against.
- I want to know if I consistently die too early in games.
- I want to know if I perform better at certain times of the day or week.
- I want to understand which enemy junglers I struggle against.
- I want to understand how objective control (such as Dragon Souls) impacts my win rate.

---

# Business Questions

1. Which champions do I perform best on?
2. Am I improving over time?
3. Do I perform better at certain times of the day or week?
4. Which champion matchups do I struggle against?
5. Am I dying too early in games?
6. Which enemy junglers do I lose to the most?
7. Which champions should I stop playing?
8. How much do Dragon Souls impact my chances of winning?

---

# Metrics

## Performance

- Win Rate
- Games Played
- KDA
- CS/min
- Damage/min
- Vision Score

## Early Game

- Average First Death Time
- First Blood Victim Rate
- Deaths Before 5 Minutes
- Deaths Before 10 Minutes

## Objectives

- Dragon Soul Win Rate
- Win Rate by Dragon Soul Type
- First Dragon Win Rate

## Time

- Win Rate by Hour
- Win Rate by Day of Week

---

# Version 1 Scope

The first version of this project should answer these questions:

- What are my best champions?
- Am I improving over time?
- Do I perform better at certain times?
- Which champion matchups do I struggle against?
- Am I dying too early?
- Which enemy junglers beat me the most?
- Which champions should I stop playing?
- How much do Dragon Souls contribute to winning?

---

# Future Features

- Compare my stats against players in the same rank.
- AI-generated coaching recommendations.
- Champion recommendation system.
- Lane matchup heatmaps.
- Rune and item effectiveness analysis.
- Team composition analysis.
- Draft recommendations.
- LP prediction.