import numpy as np
from server import get_connection


def fetch_array(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return np.array(rows, dtype=object)


def show_info(name, arr):
    print(f"{name} shape: {arr.shape} dtype: {arr.dtype}")


def to_float_nan(arr_obj):
    return np.where(arr_obj == None, np.nan, arr_obj).astype(float)


def probability(mask, denom):
    return (np.count_nonzero(mask) / denom) * 100.0 if denom > 0 else 0.0


def main():
    conn = get_connection()
    cursor = conn.cursor()

    data = fetch_array(
        cursor,
        """
        SELECT
            m.runtime,
            m.genre,
            r.rating,
            m.year_of_release,
            c.country,
            c.gender
        FROM rentings r
        JOIN movies m
            ON m.movie_id = r.movie_id
        JOIN customers c
            ON c.customer_id = r.customer_id
        """
    )

    if data.size == 0:
        print("Not enough data to run Person 1 (no rows returned).")
        cursor.close()
        conn.close()
        return

    runtime_obj = data[:, 0]
    genre = data[:, 1].astype(str)
    rating_obj = data[:, 2]
    year_obj = data[:, 3]
    country = data[:, 4].astype(str)
    gender = data[:, 5].astype(str)

    runtime = to_float_nan(runtime_obj)
    rating = to_float_nan(rating_obj)
    year_of_release = to_float_nan(year_obj)

    show_info("data", data)
    show_info("runtime", runtime)
    show_info("genre", genre)
    show_info("rating", rating)
    show_info("year_of_release", year_of_release)
    show_info("country", country)
    show_info("gender", gender)

    valid_runtime = ~np.isnan(runtime)
    denom_runtime = np.count_nonzero(valid_runtime)

    c1 = valid_runtime & (runtime < 80)
    c2 = valid_runtime & (runtime >= 80) & (runtime < 100)
    c3 = valid_runtime & (runtime >= 100) & (runtime < 120)
    c4 = valid_runtime & (runtime >= 120) & (runtime < 150)
    c5 = valid_runtime & (runtime >= 150)

    print("\nRUNTIME CATEGORY PROBABILITIES (based on available runtime values)")
    print(f"Denominator count (valid runtime): {int(denom_runtime)}")

    categories = [
        ("< 80 min", c1),
        ("80-99 min", c2),
        ("100-119 min", c3),
        ("120-149 min", c4),
        (">= 150 min", c5),
    ]

    for label, mask in categories:
        print(f"{label}: {probability(mask, denom_runtime):.2f}%")

    manual_count = np.count_nonzero(c3)
    manual_prob = probability(c3, denom_runtime)
    func_prob = probability(c3[valid_runtime], denom_runtime)

    print("\nMANUAL VERIFICATION (category 100-119 min)")
    print(f"Count in category: {int(manual_count)}")
    print(f"Manual probability: {manual_prob:.2f}%")
    print(f"Vectorized probability: {func_prob:.2f}%")

    valid_year = ~np.isnan(year_of_release)
    denom_year = np.count_nonzero(valid_year)

    for y in (2000, 2010, 2020):
        mask = valid_year & (year_of_release > float(y))
        print(f"\nProbability movie released after {y}: {probability(mask, denom_year):.2f}%")

    valid_rating = ~np.isnan(rating)
    denom_ratings = np.count_nonzero(valid_rating)
    print(f"\nProbability a rented movie has a rating: {probability(valid_rating, len(rating)):.2f}%")

    print("\nRATING VALUE PROBABILITIES (1-5, based on rated rentals)")
    for v in range(1, 6):
        mask = valid_rating & (rating == float(v))
        print(f"Rating = {v}: {probability(mask, denom_ratings):.2f}%")

    print("\nGENRE PROBABILITIES (based on rented-movie rows)")
    unique_genres, counts_genres = np.unique(genre, return_counts=True)
    denom_genre = len(genre)
    for g, cnt in zip(unique_genres, counts_genres):
        p = (cnt / denom_genre) * 100.0 if denom_genre > 0 else 0.0
        print(f"{g}: {p:.2f}%")

    print("\nCOUNTRY PROBABILITIES (based on rental rows)")
    unique_countries, counts_countries = np.unique(country, return_counts=True)
    denom_country = len(country)
    for ct, cnt in zip(unique_countries, counts_countries):
        p = (cnt / denom_country) * 100.0 if denom_country > 0 else 0.0
        print(f"{ct}: {p:.2f}%")

    print("\nGENDER PROBABILITIES (based on rental rows)")
    unique_genders, counts_genders = np.unique(gender, return_counts=True)
    denom_gender = len(gender)
    for gd, cnt in zip(unique_genders, counts_genders):
        p = (cnt / denom_gender) * 100.0 if denom_gender > 0 else 0.0
        print(f"{gd}: {p:.2f}%")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
