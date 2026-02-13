# End-to-End SQL & Python Data Analysis Project  

Movie Rental Database – Structured Analytical Workflow

---

## Project Overview

This repository showcases a complete end-to-end data analysis pipeline built around a relational Movie Rental Database.

The project integrates:

- PostgreSQL / Supabase for structured relational data

- Python (CLI Application) for automation

- NumPy for vectorized statistical computation

- Pandas for DataFrames-based EDA

- Probability & Statistical Reasoning

- Monte Carlo Simulation

- Clean project architecture and modular execution

The objective was not just to retrieve data — but to analyze, validate, interpret, and communicate insights professionally.

---

## Architecture & Design

At the core of the project:

- A reusable server.py CLI runner

- A single generic SQL execution function

- Modular script execution using runpy

- Clean separation between:

    -SQL extraction

    -Statistical computation

    -EDA

    -Reporting

This structure mirrors how production data tools are built.

## Learning Objectives

1-SQL Data Analysis

    -SELECT, WHERE, GROUP BY, HAVING

    -Multi-table JOINs

    -Aggregations (COUNT, AVG, SUM)

    -Conditional filtering

    -Business-question-driven query logic

2️-Probability & Statistics (Python + NumPy)

   -Basic and conditional probability

    -Independence testing

    -Discrete random variables

    -Expected value & variance

    -Bayes’ Theorem

    -Monte Carlo simulation

    -Correct denominator selection in conditional probability

3️-DataFrames EDA (Pandas)

    -describe() statistical summaries

   -Manual mean / median / mode computation

   -Outlier detection using IQR

    -Filtering & multi-column sorting

    -GroupBy & aggregation

    -Category frequency analysis

    -Structured reporting & conclusions

---

## Project Structure

    ```text

server.py                 → Main CLI entry point
probability/              → Probability theory exercises
numpy/                    → Vectorized statistical analysis
panda/                    → DataFrames-based EDA (Person 1–7)
SQL/                      → SQL queries & schema logic
explanations/             → Written non-technical documentation
keyskills.md              → Skills demonstrated
    ```

### Core Design: One Generic SQL Runner

At the core of the project is a single reusable function:

    ```python
def run_query(cursor, query):
    ```

---

## Example Insights Extracted

    Rental activity is concentrated in specific genres and titles
    Rating distributions skew toward positive feedback
    Revenue contribution is uneven across categories
    Certain numeric fields contain outliers affecting averages
    Conditional probabilities reveal meaningful behavioral patterns

## Data Quality Handling

    Explicit NULL handling
    Numeric coercion and cleaning
    Outlier detection
    Validation against statistical pitfalls
    Structured error handling to prevent system crashes

---

### Why this matters

This repository demonstrates the ability to:

    -Translate business questions into SQL
    -Automate analysis pipelines
    -Apply statistical reasoning correctly
    -Avoid common analytical mistakes
    -Communicate findings clearly
    -Structure a project professionally
    -It reflects both technical execution and analytical maturity.

---

All datasets are converted into NumPy arrays before analysis, ensuring that computations are efficient, scalable, and reproducible.

This section reinforces best practices in analytical computing, where data extraction, transformation, and statistical analysis are clearly separated.

## How to Run the Project

### Install dependencies

    ```bash
pip install psycopg2 python-dotenv numpy
    ```

Configure environment variables

Create a .env file with the following structure:

USER=your_user
PASSWORD=your_password
HOST=your_host
PORT=5432
DBNAME=postgres
SSLMODE=require
Run the application

    ```bash
python server.py
    ```

Use the menu to navigate through SQL tasks, probability exercises, and NumPy-based analytics.

## Result

A complete analytical workflow from raw relational data to structured insights — built with production discipline and statistical correctness.  

## Final Note

This repository is intended as a portfolio-ready demonstration of applied data analysis skills, bridging theoretical knowledge with practical implementation.
