import numpy as np
from psycopg2.extras import RealDictCursor

from server import get_connection, run_query, format_probability, format_number

# =====================================================
# PART 1: RANDOM VARIABLE X — MOVIE RATINGS (FROM DB)
# =====================================================

def load_ratings_from_db():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            rows = run_query(cur, """
                SELECT rating
                FROM public.rentings
                WHERE rating IS NOT NULL;
            """)
        ratings_arr = np.fromiter((r["rating"] for r in rows), dtype=float)
        return ratings_arr
    finally:
        if conn:
            conn.close()

ratings = load_ratings_from_db()

if ratings.size == 0:
    print("No ratings found in the database (rentings.rating is empty or NULL).")
    raise SystemExit(0)

print("Raw ratings sample:", ratings[:10])

# -----------------------------------------------------
# Step 1: Identify support of X (unique values)
# -----------------------------------------------------

x_values, counts = np.unique(ratings, return_counts=True)

print("\nPossible values of X (ratings):")
print(x_values)

print("\nCounts for each rating:")
print(counts)

# -----------------------------------------------------
# Step 2: Compute PMF using normalization
# PMF = counts / total observations
# -----------------------------------------------------

total_obs = ratings.size
pmf_X = counts / total_obs

print("\nProbability Mass Function P(X = x):")
for x, p in zip(x_values, pmf_X):
    print(f"P(X={int(x)}) = {format_probability(float(p))}")


# -----------------------------------------------------
# Step 3: Expected Value using dot product
# E(X) = Σ x · P(X=x)
# -----------------------------------------------------

expected_X = np.dot(x_values, pmf_X)

print("\nExpected Value E(X):", format_number(float(expected_X)))

print(
    "\nInterpretation:\n"
    "If we repeatedly select a rating at random from the database,\n"
    "the long-run average rating we expect to observe is {:.2f}.\n"
    "This does NOT mean most movies have this rating — it is a weighted average."
    .format(expected_X)
)

# -----------------------------------------------------
# Step 4: Variance (manual formula)
# Var(X) = Σ (x − μ)^2 · P(X=x)
# -----------------------------------------------------

deviations = x_values - expected_X
squared_deviations = deviations ** 2

print("\nDeviations from mean:")
print(deviations)

print("\nSquared deviations:")
print(squared_deviations)

variance_X = np.dot(squared_deviations, pmf_X)
std_dev_X = np.sqrt(variance_X)

print("\nVariance Var(X):", format_number(float(variance_X)))
print("\nStandard Deviation:", format_number(float(std_dev_X)))

print(
    "\nInterpretation:\n"
    "Variance measures how spread out the ratings are around the mean.\n"
    "The standard deviation tells us that ratings typically differ from\n"
    "the average by about {:.2f} rating points."
    .format(std_dev_X)
)

# -----------------------------------------------------
# Step 5: Manual sanity check on small subset
# -----------------------------------------------------

subset = x_values[:3]
subset_pmf = pmf_X[:3]

manual_check = subset[0]*subset_pmf[0] + subset[1]*subset_pmf[1] + subset[2]*subset_pmf[2]

print(
    "\nManual verification (partial sum of E(X) using first 3 values):",
    manual_check
)

