"""
Discrete Random Variables
Probability & Statistics with Python
Movie Rental System

This script models real-world quantities from the movie rental database
as discrete random variables and explains what each statistical result means.
All formulas are implemented manually, without using any probability libraries.
"""

# =====================================================
# PART 1: MOVIE RATING AS DISCRETE RANDOM VARIABLE (X)
# =====================================================

# X represents the rating of a randomly selected movie.
# Ratings are discrete numeric values, so X is a discrete random variable.

# The following dictionary was obtained using SQL:
# SELECT rating, COUNT(*) FROM movies WHERE rating IS NOT NULL GROUP BY rating;

rating_counts = {
    1.59: 8,
    1.69: 6,
    1.79: 8,
    2.09: 6,
    2.59: 5,
    2.69: 7,
    2.89: 6,
    3.09: 4,
    3.39: 4,
    3.69: 4,
    3.89: 3,
    4.09: 4,
    4.39: 3,
    4.69: 2,
    4.89: 1
}

# Total number of rated movies in the database
total_movies = sum(rating_counts.values())


# -----------------------------------------------------
# Probability Mass Function (PMF) of X
# P(X = x) = number of movies with rating x / total movies
# -----------------------------------------------------

pmf_X = {}

for rating, count in rating_counts.items():
    pmf_X[rating] = count / total_movies


# -----------------------------------------------------
# Expected Value of X
# Formula: E(X) = Σ x · P(X = x)
# -----------------------------------------------------

expected_X = 0

for x, p in pmf_X.items():
    expected_X += x * p


# -----------------------------------------------------
# Variance of X
# Formula: Var(X) = Σ (x − μ)² · P(X = x)
# -----------------------------------------------------

variance_X = 0

for x, p in pmf_X.items():
    variance_X += (x - expected_X) ** 2 * p


# Standard deviation gives dispersion in original units
std_dev_X = variance_X ** 0.5


# =====================================================
# INTERPRETATION OF RESULTS FOR X
# =====================================================

print("----- RANDOM VARIABLE X: MOVIE RATING -----\n")

print(f"Expected Value E(X) = {expected_X:.3f}")
print(
    "Interpretation:\n"
    "If we repeatedly and randomly select movies from the database,\n"
    "the average rating we would observe in the long run is approximately "
    f"{expected_X:.2f}.\n"
)

print(f"Variance Var(X) = {variance_X:.3f}")
print(
    "Interpretation:\n"
    "The variance measures how spread out the movie ratings are around\n"
    "the average rating. A relatively small variance indicates that most\n"
    "ratings are not very far from the mean.\n"
)

print(f"Standard Deviation = {std_dev_X:.3f}")
print(
    "Interpretation:\n"
    "The standard deviation tells us that most movie ratings typically\n"
    "differ from the average rating by about "
    f"{std_dev_X:.2f} points.\n"
)


# =====================================================
# PART 2: MOVIES RENTED PER CUSTOMER AS RANDOM VARIABLE (Y)
# =====================================================

# Y represents the number of movies rented by a randomly selected customer.
# This is a discrete random variable because rentals are whole numbers.

# This data was extracted using SQL:
# SELECT customer_id, COUNT(*) FROM rentings GROUP BY customer_id;

rentals_per_customer_counts = {
    1: 7,
    2: 5,
    3: 9,
    4: 8,
    5: 7,
    6: 6,
    7: 5,
    8: 4,
    9: 4,
    10: 3
}

# Total number of customers
total_customers = sum(rentals_per_customer_counts.values())


# -----------------------------------------------------
# PMF of Y
# P(Y = y) = number of customers who rented y movies / total customers
# -----------------------------------------------------

pmf_Y = {}

for rentals, count in rentals_per_customer_counts.items():
    pmf_Y[rentals] = count / total_customers


# -----------------------------------------------------
# Expected Value of Y
# Formula: E(Y) = Σ y · P(Y = y)
# -----------------------------------------------------

expected_Y = 0

for y, p in pmf_Y.items():
    expected_Y += y * p


# -----------------------------------------------------
# Variance of Y
# -----------------------------------------------------

variance_Y = 0

for y, p in pmf_Y.items():
    variance_Y += (y - expected_Y) ** 2 * p


# =====================================================
# INTERPRETATION OF RESULTS FOR Y
# =====================================================

print("----- RANDOM VARIABLE Y: MOVIES RENTED PER CUSTOMER -----\n")

print(f"Expected Value E(Y) = {expected_Y:.3f}")
print(
    "Interpretation:\n"
    "This means that if we randomly select customers repeatedly,\n"
    "the average number of movies rented per customer will converge\n"
    f"to approximately {expected_Y:.0f} movies.\n"
)

print(f"Variance Var(Y) = {variance_Y:.3f}")
print(
    "Interpretation:\n"
    "The large variance indicates that customer behavior varies widely.\n"
    "Some customers rent only a few movies, while others rent many more,\n"
    "leading to significant dispersion around the average.\n"
)
