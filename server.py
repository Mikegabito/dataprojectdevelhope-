import os
import time
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Iterable, Tuple

import runpy

import psycopg2
from psycopg2 import Error as PsycopgError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# DB CONFIG
# -------------------------------------------------------------------
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
SSLMODE = os.getenv("SSLMODE", "require")

SHOW_QUERY_TIME = os.getenv("SHOW_QUERY_TIME", "0") == "1"

_LAST_RESULT: List[Dict[str, Any]] = []

def _require_env():
    missing = [k for k, v in {
        "USER": USER,
        "PASSWORD": PASSWORD,
        "HOST": HOST,
        "PORT": PORT,
        "DBNAME": DBNAME,
    }.items() if not v]
    if missing:
        raise ValueError(
            "Missing required .env variables: "
            + ", ".join(missing)
            + ". Please set them in your .env file."
        )

def get_connection():
    """Create and return a DB connection."""
    _require_env()
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE,
    )

# -------------------------------------------------------
# Task 1 – Generic Function (all queries go through here)
# -------------------------------------------------------
def run_query(cursor, query):
    """
    Executes ANY SQL query and returns results for SELECT queries.

    Task 9 requirement:
    - If SQL is invalid, catch exception, print friendly message, and do NOT crash.
    """
    global _LAST_RESULT

    start = time.perf_counter()
    try:
        cursor.execute(query)

        if cursor.description is not None:
            rows = cursor.fetchall()

            _LAST_RESULT = [dict(r) for r in rows]

            if SHOW_QUERY_TIME:
                elapsed_ms = (time.perf_counter() - start) * 1000
                print(f"[Query time: {elapsed_ms:.2f} ms]")

            return _LAST_RESULT

        cursor.connection.commit()
        _LAST_RESULT = []
        return []

    except PsycopgError as e:
        try:
            cursor.connection.rollback()
        except Exception:
            pass

        msg = getattr(e, "pgerror", None) or str(e)
        print("\n[SQL ERROR] Your query could not be executed.")
        print(f"Details: {msg.strip()}")
        _LAST_RESULT = []
        return []

    except Exception as e:
        try:
            cursor.connection.rollback()
        except Exception:
            pass
        print("\n[ERROR] Unexpected error while executing query.")
        print(f"Details: {e}")
        _LAST_RESULT = []
        return []

# -------------------------------------------------------
# Generic fetch function (keeps the style used in your file)
# -------------------------------------------------------
def _fetch_all(query: str) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            return run_query(cur, query)
    finally:
        if conn:
            conn.close()

# ============================
# Task 8 – Output Formatting
# ============================
def _format_value(v: Any) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def _print_rows(title: str, rows: List[Dict[str, Any]], max_rows: int = 20) -> None:
    """Pretty, labeled printing for any list of dict rows."""
    print(f"\n===== {title} =====")
    if not rows:
        print("No data found.")
        return

    to_show = rows[:max_rows]
    for i, row in enumerate(to_show, start=1):
        parts = [f"{k}: {_format_value(v)}" for k, v in row.items()]
        print(f"{i}. " + " | ".join(parts))

    if len(rows) > max_rows:
        print(f"... ({len(rows) - max_rows} more rows not shown)")


# -------------------------------------------------------
# Task Bonus – Save last results to a file
# -------------------------------------------------------
def save_last_result_json(filepath: str = "last_result.json") -> None:
    if not _LAST_RESULT:
        print("No last result to save.")
        return
    Path(filepath).write_text(json.dumps(_LAST_RESULT, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved last result to {filepath}")


def save_last_result_csv(filepath: str = "last_result.csv") -> None:
    if not _LAST_RESULT:
        print("No last result to save.")
        return
    headers = sorted({k for row in _LAST_RESULT for k in row.keys()})
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(_LAST_RESULT)
    print(f"Saved last result to {filepath}")

# ============================
# Task 2 – SELECT queries
# ============================
def get_all_movies(cursor):
    query = "SELECT * FROM movies;"
    return run_query(cursor, query)

def get_all_customers(cursor):
    query = "SELECT * FROM customers;"
    return run_query(cursor, query)

def get_all_actors(cursor):
    query = "SELECT * FROM actors;"
    return run_query(cursor, query)

# ---------------------------------------------------------
# Convenience fetchers (already used by your menu)
# ---------------------------------------------------------
def fetch_actors():
    rows = _fetch_all("SELECT * FROM public.actors;")
    _print_rows("ACTORS", rows)
    return rows

def fetch_actsin():
    rows = _fetch_all("SELECT * FROM public.actsin;")
    _print_rows("ACTSIN", rows)
    return rows

def fetch_customers():
    rows = _fetch_all("SELECT * FROM public.customers;")
    _print_rows("CUSTOMERS", rows)
    return rows

def fetch_log_activity():
    rows = _fetch_all("SELECT * FROM public.log_activity;")
    _print_rows("LOG_ACTIVITY", rows)
    return rows

def fetch_movies():
    rows = _fetch_all("SELECT * FROM public.movies;")
    _print_rows("MOVIES", rows)
    return rows

def fetch_rentings():
    rows = _fetch_all("SELECT * FROM public.rentings;")
    _print_rows("RENTINGS", rows)
    return rows

def fetch_view_actor_summary():
    rows = _fetch_all("SELECT * FROM public.view_actor_summary;")
    _print_rows("VIEW_ACTOR_SUMMARY", rows)
    return rows

# ============================
# Task 3 – WHERE Clause
# ============================
def fetch_task3_movies_after_2015():
    rows = _fetch_all("SELECT * FROM public.movies WHERE year_of_release > 2015;")
    _print_rows("TASK3_MOVIES_AFTER_2015", rows)
    return rows

def fetch_task3_customers_from_canada():
    rows = _fetch_all("SELECT * FROM public.customers WHERE country = 'Canada';")
    _print_rows("TASK3_CUSTOMERS_FROM_CANADA", rows)
    return rows

def fetch_task3_rentings_rating_ge_4():
    rows = _fetch_all("SELECT * FROM public.rentings WHERE rating >= 4;")
    _print_rows("TASK3_RENTINGS_RATING_GE_4", rows)
    return rows

# ============================
# Task 4 – Aggregation Functions
# ============================
def get_total_movies(cursor):
    query = """
    SELECT COUNT(movie_id) AS total_movies
    FROM movies;
    """
    return run_query(cursor, query)


def get_total_customers(cursor):
    query = """
    SELECT COUNT(customer_id) AS total_customers
    FROM customers;
    """
    return run_query(cursor, query)

def get_average_movie_rating(cursor):
    query = """
    SELECT AVG(rating) AS avg_rating
    FROM rentings
    WHERE rating IS NOT NULL;
    """
    return run_query(cursor, query)

# ============================
# Task 5 – GROUP BY
# ============================
def get_number_of_movies_per_genre(cursor):
    query = """
    SELECT
        genre,
        COUNT(movie_id) AS movie_count
    FROM movies
    GROUP BY genre
    ORDER BY movie_count DESC;
    """
    return run_query(cursor, query)

def get_number_of_customers_per_country(cursor):
    query = """
    SELECT
        country,
        COUNT(customer_id) AS customer_count
    FROM customers
    GROUP BY country
    ORDER BY customer_count DESC;
    """
    return run_query(cursor, query)

def get_number_of_rentings_per_movie(cursor):
    query = """
    SELECT
        m.title,
        COUNT(r.renting_id) AS renting_count
    FROM movies m
    JOIN rentings r
        ON r.movie_id = m.movie_id
    GROUP BY m.title
    ORDER BY renting_count DESC;
    """
    return run_query(cursor, query)

# ============================
# Task 6 – JOIN Queries
# ============================
def get_movies_with_avg_rating(cursor):
    query = """
    SELECT
      movie_id,
      title,
      avg_rating
    FROM movies
    ORDER BY avg_rating DESC NULLS LAST;
    """
    return run_query(cursor, query)


def get_actors_with_movie_count(cursor):
    query = """
    SELECT
      a.actor_id,
      a.name AS actor_name,
      COUNT(ac.movie_id) AS movie_count
    FROM actors a
    LEFT JOIN actsin ac ON ac.actor_id = a.actor_id
    GROUP BY a.actor_id, a.name
    ORDER BY movie_count DESC;
    """
    return run_query(cursor, query)


def get_customers_with_rentals_count(cursor):
    query = """
    SELECT
      c.customer_id,
      c.name AS customer_name,
      COUNT(r.renting_id) AS rentals_count
    FROM customers c
    LEFT JOIN rentings r ON r.customer_id = c.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY rentals_count DESC;
    """
    return run_query(cursor, query)

# ============================
# Task 7 – HAVING Clause
# ============================
def get_genres_with_more_than_3_movies(cursor):
    query = """
    SELECT
        genre,
        COUNT(movie_id) AS total_movies
    FROM movies
    GROUP BY genre
    HAVING COUNT(movie_id) > 3
    ORDER BY total_movies DESC;
    """
    return run_query(cursor, query)

def get_movies_with_avg_rating_above_4(cursor):
    query = """
    SELECT
        movie_id,
        title,
        genre,
        avg_rating
    FROM movies
    GROUP BY movie_id, title, genre, avg_rating
    HAVING avg_rating > 4
    ORDER BY avg_rating DESC;
    """
    return run_query(cursor, query)

def get_customers_with_more_than_5_rentals(cursor):
    query = """
    SELECT
        c.customer_id,
        COUNT(r.renting_id) AS total_rentals
    FROM customers c
    JOIN rentings r
        ON r.customer_id = c.customer_id
    GROUP BY c.customer_id
    HAVING COUNT(r.renting_id) > 5
    ORDER BY total_rentals DESC;
    """
    return run_query(cursor, query)


BASE_DIR = Path(__file__).resolve().parent

def _run_script(relative_path: str) -> None:
    """Run a .py file as a script (safe for circular-import issues)."""
    script_path = BASE_DIR / relative_path
    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        return

    print(f"\n--- Running: {relative_path} ---\n")
    runpy.run_path(str(script_path), run_name="__main__")


def show_probability_menu():
    print("\n=== PROBABILITY HOMEWORK ===")
    print("1. Person 1 - Basic Probability")
    print("2. Person 2 - Conditional Probability")
    print("3. Person 3 - Independent Events")
    print("4. Discrete Random Variables")
    print("5. Monte Carlo (Nelson)")
    print("6. Person 6 - Bayes Theorem")
    print("0. Back")


def handle_probability_menu():
    while True:
        show_probability_menu()
        ch = input("\nEnter your choice: ").strip()

        if ch == "0":
            break
        elif ch == "1":
            _run_script("probability/person1_basic_probability.py")
        elif ch == "2":
            _run_script("probability/person2_conditional_probability.py")
        elif ch == "3":
            _run_script("probability/person3_independent_events.py")
        elif ch == "4":
            _run_script("probability/DiscreteRandVar.py")
        elif ch == "5":
            _run_script("probability/montecarlo_nelson.py")
        elif ch == "6":
            _run_script("probability/person6_bayes_theorem.py")
        else:
            print("Invalid option.")

def show_numpy_menu():
    print("\n=== NUMPY PROBABILITY HOMEWORK ===")
    print("1. Task 1 - Vectorized Probability Distributions (Person1)")
    print("2. Task 2 - Conditional Probability with NumPy Masks (Person2)")
    print("3. Task 3 - Independence Testing (Person3)")
    print("4. Task 4 - Random Variables (DiscreteVarNumpy)")
    print("5. Task 5 - Monte Carlo Simulation (Nelson)")
    print("6. Task 6 - Bayes Theorem (Person6)")
    print("7. Task 7 - Statistical Experiments & Reporting (Person7)")
    print("0. Back")


def handle_numpy_menu():
    while True:
        show_numpy_menu()
        ch = input("\nEnter your choice: ").strip()

        if ch == "0":
            break
        elif ch == "1":
            _run_script("numpy/person1_numpy_task1.py")
        elif ch == "2":
            _run_script("numpy/Person2_Conditional_Probability_with_NumPy_Masks.py")
        elif ch == "3":
            _run_script("numpy/person3_numpy_task3.py")
        elif ch == "4":
            _run_script("numpy/DiscreteVarNumpy.py")
        elif ch == "5":
            _run_script("numpy/montecarlonumpyT5_nelson.py")
        elif ch == "6":
            _run_script("numpy/person6_numpy_task6.py")
        elif ch == "7":
            _run_script("numpy/person7_numpy_task7.py")
        else:
            print("Invalid option.")



# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------
def show_menu():
    print("\n=== PYTHON & SQL QUERY RUNNER (Assignment Tasks) ===")

    print("\n--- Task 2: Basic SELECT Queries ---")
    print("1. Retrieve all movies")
    print("2. Retrieve all customers")
    print("3. Retrieve all actors")

    print("\n--- Task 3: WHERE Clause ---")
    print("4. Movies released after 2015")
    print("5. Customers from Canada")
    print("6. Rentings with rating >= 4")

    print("\n--- Task 4: Aggregation Functions (COUNT, AVG) ---")
    print("7. Total number of movies")
    print("8. Average renting price of movies")
    print("9. Average rating from rentings")

    print("\n--- Task 5: GROUP BY ---")
    print("10. Number of movies per genre")
    print("11. Number of customers per country")
    print("12. Number of rentings per movie")

    print("\n--- Task 6: JOIN Queries ---")
    print("13. Movie titles with their average rating")
    print("14. Number of movies each actor acted in")
    print("15. Number of movies rented by each customer")

    print("\n--- Task 7: HAVING Clause ---")
    print("16. Genres with more than 3 movies")
    print("17. Movies with average rating above 4")
    print("18. Customers who rented more than 5 movies")

    print("\n--- Task 9: Error Handling ---")
    print("19. Run an INVALID query (should not crash)")

    print("\n--- Bonus Tasks ---")
    print("20. Save last result as JSON")
    print("21. Save last result as CSV")

    print("\n--- Extra ---")
    print("P. Probability Homework (run scripts)")

    print("\n--- Extra ---")
    print("N. NumPy Probability Homework")

    print("\n0. Exit")

def fetch_task4_total_movies():
    rows = _fetch_all("SELECT COUNT(movie_id) AS total_movies FROM public.movies;")
    _print_rows("TASK4_TOTAL_MOVIES", rows)
    return rows

def fetch_task4_avg_renting_price():
    rows = _fetch_all("""
        SELECT AVG(renting_price) AS avg_renting_price
        FROM public.movies
        WHERE renting_price IS NOT NULL;
    """)
    _print_rows("TASK4_AVG_RENTING_PRICE", rows)
    return rows

def fetch_task4_avg_rating():
    rows = _fetch_all("SELECT AVG(rating) AS avg_rating FROM public.rentings WHERE rating IS NOT NULL;")
    _print_rows("TASK4_AVG_RATING", rows)
    return rows

def _task9_invalid_query_demo():
    print("\n=== Task 9 Demo: invalid SQL (should not crash) ===")
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            run_query(cur, "SELECT * FROM this_table_does_not_exist;")
    finally:
        if conn:
            conn.close()

def _handle_choice(choice: str) -> bool:
    """Returns True if program should continue, False to exit."""
    if choice == "1":
        # Task 2
        rows = _fetch_all("SELECT * FROM public.movies;")
        _print_rows("TASK2_ALL_MOVIES", rows)

    elif choice == "2":
        # Task 2
        rows = _fetch_all("SELECT * FROM public.customers;")
        _print_rows("TASK2_ALL_CUSTOMERS", rows)

    elif choice == "3":
        # Task 2
        rows = _fetch_all("SELECT * FROM public.actors;")
        _print_rows("TASK2_ALL_ACTORS", rows)

    elif choice == "4":
        fetch_task3_movies_after_2015()

    elif choice == "5":
        fetch_task3_customers_from_canada()

    elif choice == "6":
        fetch_task3_rentings_rating_ge_4()

    elif choice == "7":
        fetch_task4_total_movies()

    elif choice == "8":
        fetch_task4_avg_renting_price()

    elif choice == "9":
        fetch_task4_avg_rating()

    elif choice == "10":
        rows = _fetch_all("""SELECT genre, COUNT(movie_id) AS movie_count
                            FROM public.movies
                            GROUP BY genre
                            ORDER BY movie_count DESC;""")
        _print_rows("TASK5_MOVIES_PER_GENRE", rows)

    elif choice == "11":
        rows = _fetch_all("""SELECT country, COUNT(customer_id) AS customer_count
                            FROM public.customers
                            GROUP BY country
                            ORDER BY customer_count DESC;""")
        _print_rows("TASK5_CUSTOMERS_PER_COUNTRY", rows)

    elif choice == "12":
        rows = _fetch_all("""SELECT m.title, COUNT(r.renting_id) AS renting_count
                            FROM public.movies m
                            JOIN public.rentings r ON r.movie_id = m.movie_id
                            GROUP BY m.title
                            ORDER BY renting_count DESC;""")
        _print_rows("TASK5_RENTINGS_PER_MOVIE", rows)

    elif choice == "13":
        # Task 6
        rows = _fetch_all("""
            SELECT
              m.title,
              AVG(r.rating) AS avg_rating
            FROM public.movies m
            JOIN public.rentings r ON r.movie_id = m.movie_id
            WHERE r.rating IS NOT NULL
            GROUP BY m.title
            ORDER BY avg_rating DESC;
        """)
        _print_rows("TASK6_MOVIES_WITH_AVG_RATING", rows)

    elif choice == "14":
        # Task 6
        rows = _fetch_all("""
            SELECT
              a.name AS actor_name,
              COUNT(ac.movie_id) AS movie_count
            FROM public.actors a
            LEFT JOIN public.actsin ac ON ac.actor_id = a.actor_id
            GROUP BY a.name
            ORDER BY movie_count DESC;
        """)
        _print_rows("TASK6_ACTORS_MOVIE_COUNT", rows)

    elif choice == "15":
        # Task 6
        rows = _fetch_all("""
            SELECT
              c.name AS customer_name,
              COUNT(r.renting_id) AS rentals_count
            FROM public.customers c
            LEFT JOIN public.rentings r ON r.customer_id = c.customer_id
            GROUP BY c.name
            ORDER BY rentals_count DESC;
        """)
        _print_rows("TASK6_CUSTOMERS_RENTALS_COUNT", rows)

    elif choice == "16":
        # Task 7
        rows = _fetch_all("""
            SELECT genre, COUNT(movie_id) AS total_movies
            FROM public.movies
            GROUP BY genre
            HAVING COUNT(movie_id) > 3
            ORDER BY total_movies DESC;
        """)
        _print_rows("TASK7_GENRES_GT_3_MOVIES", rows)

    elif choice == "17":
        # Task 7
        rows = _fetch_all("""
            SELECT
              m.title,
              AVG(r.rating) AS avg_rating
            FROM public.movies m
            JOIN public.rentings r ON r.movie_id = m.movie_id
            WHERE r.rating IS NOT NULL
            GROUP BY m.title
            HAVING AVG(r.rating) > 4
            ORDER BY avg_rating DESC;
        """)
        _print_rows("TASK7_MOVIES_AVG_RATING_GT_4", rows)

    elif choice == "18":
        # Task 7
        rows = _fetch_all("""
            SELECT
              c.name AS customer_name,
              COUNT(r.renting_id) AS total_rentals
            FROM public.customers c
            JOIN public.rentings r ON r.customer_id = c.customer_id
            GROUP BY c.name
            HAVING COUNT(r.renting_id) > 5
            ORDER BY total_rentals DESC;
        """)
        _print_rows("TASK7_CUSTOMERS_GT_5_RENTALS", rows)

    elif choice == "19":
        _task9_invalid_query_demo()

    elif choice == "20":
        save_last_result_json()

    elif choice == "21":
        save_last_result_csv()

    elif choice == "0":
        print("Exiting...")
        return False
    
    elif choice.upper() == "P":
        handle_probability_menu()

    elif choice.upper() == "N":
        handle_numpy_menu()

    else:
        print("Invalid option, try again.")

    return True

if __name__ == "__main__":
    while True:
        try:
            show_menu()
            choice = input("\nEnter your choice: ").strip()
            if not _handle_choice(choice):
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

def format_probability(p, decimals: int = 2) -> str:
    try:
        if p is None:
            return "N/A"
        if isinstance(p, float) and (p != p):
            return "N/A"
        return f"{p * 100:.{decimals}f}%"
    except Exception:
        return "N/A"

def format_number(x, decimals: int = 2) -> str:
    try:
        if x is None:
            return "N/A"
        if isinstance(x, float) and (x != x): 
            return "N/A"
        return f"{x:.{decimals}f}"
    except Exception:
        return "N/A"
