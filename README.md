# League of Legends Analytics Engineering Pipeline

## Project Overview

The goal of this project is to learn and apply data engineering and analytics engineering concepts through hands-on experience.

I chose League of Legends because it's something I'm passionate about, and I wanted to build a project around data I genuinely find interesting.

The idea is to create an analytics service that helps my friends and other players understand their performance in ranked League of Legends, identify areas for improvement, and track their progress over time.

## Project Development

### 1. Data Ingestion — Python, Riot API, and Snowflake

I started by building a basic Python pipeline to retrieve match data from the Riot Games API and load the raw JSON into Snowflake.

My initial goal was simply to get data from the API into a data warehouse before worrying about optimization or best practices.

### 2. Data Transformation — dbt and Data Modeling

Next, I began learning dbt fundamentals and dimensional data modeling.

I approached the models from a business perspective, thinking about what information players would want to see and how the data should be structured to answer those questions.

This includes analyzing individual match performance, champion performance, and ranked progression.

### 3. Pipeline Improvements — Current Focus

I'm currently revisiting my Python ingestion pipeline to improve its structure, reliability, error handling, and overall code quality.

My goal is to move beyond a script that simply works and learn how to build a maintainable, production-style data pipeline.

Once I'm satisfied with the ingestion process, I plan to revisit and improve my dbt models using the same approach.

### 4. Reporting and Visualization — Planned

The final phase will be to connect the transformed data to Looker and build dashboards that present useful insights into player performance.

The goal is to make the data easy to understand and actionable for someone trying to improve at League of Legends.

## Project Status

**Work in progress.**

This project is primarily a learning experience. I'm continuously improving it as I learn more about Python, Snowflake, dbt, data modeling, and analytics engineering best practices.

## Learning Approach

I use documentation, online resources, and AI tools to help me learn and develop this project.

AI has been useful for understanding unfamiliar concepts, troubleshooting errors, reviewing code, and exploring better implementation approaches.

My goal is to understand the code I write, the decisions behind it, and how to improve the pipeline as I develop my skills.
