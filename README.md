# SQL & Python Data Analysis Project  

Movie Database – End-to-End Data Analyst Practice

---

## Project Overview

This repository contains a complete end-to-end data analysis project built around a Movie Database, combining:

- SQL (PostgreSQL / Supabase) for data storage and querying  
- Python for automation and analytics  
- NumPy for vectorized probability calculations  
- Statistical reasoning applied to real datasets  

The project simulates real-world Data Analyst workflows, from data extraction to analytical insight, emphasizing clean structure, correctness, and reproducibility.

---

## Learning Objectives

This project demonstrates the ability to:

- Query relational databases using SQL best practices  
- Execute SQL safely from Python using a generic query runner  
- Apply filtering, aggregation, grouping, joins, and HAVING clauses  
- Implement error handling in data pipelines  
- Use NumPy vectorization instead of loops for probability calculations  
- Correctly compute conditional probability, expected value, variance, and Monte Carlo simulations  
- Organize a project in a production-ready structure  
- Explain analytical results in clear, non-technical language  

---

## Project Structure

```text
SQL-TEAM-PROJECT/
│
├── server.py                # Main CLI application (SQL + Python integration)
├── .env                     # Local DB credentials (not committed)
├── README.md
│
├── SQL/                      # SQL scripts (schema, views, queries)
│
├── probability/              # Pure Python probability exercises
│   ├── person1_basic_probability.py
│   ├── person2_conditional_probability.py
│   ├── person3_independent_events.py
│   ├── DiscreteRandVar.py
│   ├── montecarlo_nelson.py
│   └── person6_bayes_theorem.py
│
├── numpy/                    # NumPy-based probability & statistics
│   ├── person1_numpy_task1.py
│   ├── Person2_Conditional_Probability_with_NumPy_Masks.py
│   ├── person3_numpy_task3.py
│   ├── DiscreteVarNumpy.py
│   ├── montecarlonumpyT5_nelson.py
│   ├── person6_numpy_task6.py
│   └── person7_numpy_task7.py
│
└── explanations/             # Written explanations and documentation
```

### Core Design: One Generic SQL Runner

At the core of the project is a single reusable function:

```python
def run_query(cursor, query):
```

All SQL queries are executed through this function.

### Why this matters

- Enforces consistency across the project  
- Centralizes error handling  
- Prevents duplicated logic  
- Mirrors how real data services and APIs are designed  

This design reflects professional backend and analytics engineering practices.

SQL Tasks (server.py)
All SQL tasks are accessible through a menu-driven CLI.

Task 2 – Basic SELECT Queries
Purpose: Practice simple data retrieval.

- Retrieve all movies

- Retrieve all customers

- Retrieve all actors

Why it matters:
These queries represent the foundation of exploratory data analysis.

Task 3 – WHERE Clause
Purpose: Filter records using conditions.

- Movies released after 2015

- Customers from Canada

- Rentings with rating greater than or equal to 4

Why it matters:
Filtering enables segmentation and targeted analysis.

Task 4 – Aggregation Functions (COUNT, AVG)
Purpose: Summarize datasets.

- Total number of movies

- Average renting price of movies

- Average rating from rentings

Why it matters:
Aggregations transform raw data into meaningful metrics and KPIs.

Task 5 – GROUP BY
Purpose: Analyze distributions.

- Number of movies per genre

- Number of customers per country

- Number of rentings per movie

Why it matters:
Grouping reveals patterns, trends, and imbalances in the data.

Task 6 – JOIN Queries
Purpose: Combine data from multiple tables.

- Movie titles with their average rating

- Number of movies each actor acted in

- Number of movies rented by each customer

Why it matters:
JOIN operations are essential for relational data analysis.

Task 7 – HAVING Clause
Purpose: Filter aggregated results.

- Genres with more than three movies

- Movies with average rating above four

- Customers who rented more than five movies

Why it matters:
HAVING enables filtering based on aggregated conditions rather than raw rows.

Task 9 – Error Handling
Purpose: Ensure robustness.

- Execute an invalid SQL query

- Catch exceptions

- Prevent application crashes

Why it matters:
Reliable data systems must fail gracefully.

## Probability (Pure Python)

The probability/ folder focuses on statistical reasoning independent of databases.

Topics covered include:

- Basic probability

- Conditional probability

- Independent vs dependent events

- Discrete random variables

- Monte Carlo simulations

- Bayes’ Theorem

Why it matters:
A Data Analyst must understand probability to correctly interpret data, not just compute values.

## NumPy Probability & Statistics

The `numpy/` folder applies probability and statistics concepts using NumPy on real data retrieved from the project database.

Each exercise focuses on vectorized computation and correct statistical reasoning, avoiding loops and hardcoded probabilities.

Covered topics include:

- Vectorized probability calculations using NumPy arrays  
- Boolean masks to represent events  
- Conditional probability and correct denominator selection  
- Discrete random variables and probability mass functions  
- Expected value, variance, and standard deviation  
- Monte Carlo simulations  
- Bayesian probability  

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

Final Note
This repository is intended as a portfolio-ready demonstration of applied data analysis skills, bridging theoretical knowledge with practical implementation.
