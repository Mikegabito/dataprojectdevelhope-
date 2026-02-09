import numpy as np
from psycopg2.extras import RealDictCursor
from server import get_connection, run_query

"""
Task 2 – Conditional Probability using NumPy Boolean Masks
Data source: Supabase PostgreSQL (rentings + movies)
"""

# --------------------------------------------------
# Load data from DB
# --------------------------------------------------

def load_data():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            rows = run_query(cur, """
                SELECT
                    m.genre,
                    m.runtime,
                    r.rating
                FROM public.rentings r
                JOIN public.movies m
                    ON r.movie_id = m.movie_id;
            """)

        genres = np.array([row["genre"] for row in rows], dtype=str)
        runtimes = np.array([row["runtime"] for row in rows], dtype=int)
        ratings = np.array(
            [row["rating"] if row["rating"] is not None else np.nan for row in rows],
            dtype=float
        )

        return genres, runtimes, ratings

    finally:
        if conn:
            conn.close()


genres, runtimes, ratings = load_data()

print("Array shapes and dtypes:")
print("genres:", genres.shape, genres.dtype)
print("runtimes:", runtimes.shape, runtimes.dtype)
print("ratings:", ratings.shape, ratings.dtype)

# --------------------------------------------------
# Define events
# --------------------------------------------------

A = (genres == "Comedy")          
B = (ratings >= 4)                
C = (runtimes > 120)             
D = np.isnan(ratings)             

# --------------------------------------------------
# Conditional probability function
# --------------------------------------------------

def conditional_probability(A, B):
    total_B = np.sum(B)
    if total_B == 0:
        return np.nan
    return np.sum(A & B) / total_B

# --------------------------------------------------
# Required conditional probabilities
# --------------------------------------------------

p_comedy_given_high_rating = conditional_probability(A, B)
p_high_rating_given_comedy = conditional_probability(B, A)

p_long_given_high_rating = conditional_probability(C, B)
p_high_rating_given_long = conditional_probability(B, C)

p_missing_rating_given_comedy = conditional_probability(D, A)

# --------------------------------------------------
# Output
# --------------------------------------------------

def fmt(p):
    if np.isnan(p):
        return "N/A"
    return f"{p * 100:.2f}%"

print("\nConditional Probabilities:")
print("P(Comedy | High Rating):", fmt(p_comedy_given_high_rating))
print("P(High Rating | Comedy):", fmt(p_high_rating_given_comedy))
print("P(Long Movie | High Rating):", fmt(p_long_given_high_rating))
print("P(High Rating | Long Movie):", fmt(p_high_rating_given_long))
print("P(Missing Rating | Comedy):", fmt(p_missing_rating_given_comedy))


