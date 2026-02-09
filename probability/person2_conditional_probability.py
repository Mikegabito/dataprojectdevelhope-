import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from server import format_probability

# ============================
# Load Environment Variables
# ============================

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")
SSLMODE = os.getenv("SSLMODE", "require")


def get_connection():
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE
    )

# ============================
# Helper Functions
# ============================


def run_query(query):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
    finally:
        conn.close()


def conditional_probability(total_count, favorable_count):
    """
    P(A | B) = P(A ∩ B) / P(B)
    """
    if total_count == 0:
        return 0
    return favorable_count / total_count


# ============================
# 1. P(Genre = Drama | Runtime > 100)
# ============================

def prob_drama_given_runtime_gt_100():
    movies = run_query("SELECT genre, runtime FROM movies;")

    condition = [m for m in movies if m["runtime"] > 100]
    favorable = [m for m in condition if m["genre"] == "Drama"]

    p = conditional_probability(len(condition), len(favorable))
    print(f"P(Drama | Runtime > 100) = {format_probability(p)}")


# ============================
# 2. P(Rating ≥ 4 | Genre = Comedy)
# ============================

def prob_rating_ge_4_given_comedy():
    data = run_query("""
        SELECT m.genre, r.rating
        FROM movies m
        JOIN rentings r ON r.movie_id = m.movie_id
        WHERE r.rating IS NOT NULL;
    """)

    condition = [d for d in data if d["genre"] == "Comedy"]
    favorable = [d for d in condition if d["rating"] >= 4]

    p = conditional_probability(len(condition), len(favorable))
    print(f"P(Drama | Runtime > 100) = {format_probability(p)}")


# ============================
# 3. P(Movie released after 2015 | Movie was rented)
# ============================

def prob_released_after_2015_given_rented():
    data = run_query("""
        SELECT m.year_of_release
        FROM movies m
        JOIN rentings r ON r.movie_id = m.movie_id;
    """)

    condition = data  # all rented movies
    favorable = [d for d in condition if d["year_of_release"] > 2015]

    p = conditional_probability(len(condition), len(favorable))
    print(f"P(Released after 2015 | Movie was rented) = {format_probability(p)}")


# ============================
# 4. P(Customer is Female | Customer rented ≥ 1 movie)
# ============================

def prob_female_given_rented():
    data = run_query("""
        SELECT DISTINCT c.customer_id, c.gender
        FROM customers c
        JOIN rentings r ON r.customer_id = c.customer_id;
    """)

    condition = data
    favorable = [d for d in condition if d["gender"] == "Female"]

    p = conditional_probability(len(condition), len(favorable))
    print(f"P(Female | Rented at least one movie) = {format_probability(p)}")


# ============================
# 5. P(Runtime > 120 | Year < 2000)
# ============================

def prob_runtime_gt_120_given_year_lt_2000():
    movies = run_query("""
        SELECT runtime, year_of_release
        FROM movies;
    """)

    condition = [m for m in movies if m["year_of_release"] < 2000]
    favorable = [m for m in condition if m["runtime"] > 120]

    p = conditional_probability(len(condition), len(favorable))
    print(f"P(Runtime > 120 | Release year < 2000) = {format_probability(p)}")


# ============================
# Compare Conditional vs Unconditional
# ============================

def compare_example_drama():
    movies = run_query("SELECT genre, runtime FROM movies;")

    # Unconditional P(Drama)
    drama = [m for m in movies if m["genre"] == "Drama"]
    p_unconditional = len(drama) / len(movies)

    # Conditional P(Drama | Runtime > 100)
    condition = [m for m in movies if m["runtime"] > 100]
    drama_condition = [m for m in condition if m["genre"] == "Drama"]
    p_conditional = conditional_probability(
        len(condition), len(drama_condition))

    print(f"P(Drama) = {format_probability(p_unconditional)}")
    print(f"P(Drama | Runtime > 100) = {format_probability(p_conditional)}")


# ============================
# Main
# ============================

if __name__ == "__main__":
    print("\n--- Person 2: Conditional Probability ---\n")

    prob_drama_given_runtime_gt_100()
    prob_rating_ge_4_given_comedy()
    prob_released_after_2015_given_rented()
    prob_female_given_rented()
    prob_runtime_gt_120_given_year_lt_2000()

    print("\n--- Comparison Example ---\n")
    compare_example_drama()

