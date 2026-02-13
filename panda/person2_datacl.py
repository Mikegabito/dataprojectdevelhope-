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


def probability(mask):
    n = mask.size
    return (np.count_nonzero(mask) / n) * 100.0 if n > 0 else 0.0


def conditional_probability(event_mask, given_mask):
    denom = np.count_nonzero(given_mask)
    if denom == 0:
        return 0.0
    return (np.count_nonzero(event_mask & given_mask) / denom) * 100.0


def normalize_text(arr):
    return np.char.strip(np.char.lower(arr.astype(str)))


def main():
    conn = get_connection()
    cursor = conn.cursor()

    movies = fetch_array(
        cursor,
        """
        SELECT
            movie_id,
            genre,
            runtime,
            year_of_release
        FROM movies
        """
    )

    rentals = fetch_array(
        cursor,
        """
        SELECT
            r.renting_id,
            r.customer_id,
            m.genre,
            r.rating,
            m.year_of_release
        FROM rentings r
        JOIN movies m
            ON m.movie_id = r.movie_id
        """
    )

    cust_rent = fetch_array(
        cursor,
        """
        SELECT
            c.customer_id,
            c.gender
        FROM customers c
        JOIN rentings r
            ON r.customer_id = c.customer_id
        """
    )

    if movies.size == 0 or rentals.size == 0 or cust_rent.size == 0:
        print("Not enough data to run Person 2 (one or more queries returned no rows).")
        cursor.close()
        conn.close()
        return

    show_info("movies", movies)
    show_info("rentals", rentals)
    show_info("cust_rent", cust_rent)

    movie_genre = normalize_text(movies[:, 1])
    movie_runtime = to_float_nan(movies[:, 2])
    movie_year = to_float_nan(movies[:, 3])

    rental_genre = normalize_text(rentals[:, 2])
    rental_rating = to_float_nan(rentals[:, 3])
    rental_year = to_float_nan(rentals[:, 4])

    cust_ids = cust_rent[:, 0]
    cust_gender = normalize_text(cust_rent[:, 1])

    print("\nPERSON 2 — Conditional Probability")

    given_runtime_gt_100 = ~np.isnan(movie_runtime) & (movie_runtime > 100.0)
    event_genre_drama = movie_genre == "drama"

    p_drama_given_runtime = conditional_probability(event_genre_drama, given_runtime_gt_100)
    p_drama_uncond = probability(event_genre_drama)

    print("\n1) P(Genre = Drama | Runtime > 100)")
    print(f"Conditional: {p_drama_given_runtime:.2f}%")
    print(f"Unconditional P(Drama): {p_drama_uncond:.2f}%")

    given_genre_comedy = rental_genre == "comedy"
    valid_rating = ~np.isnan(rental_rating)
    event_rating_ge_4 = valid_rating & (rental_rating >= 4.0)

    p_rating_ge_4_given_comedy = conditional_probability(event_rating_ge_4, given_genre_comedy)
    p_rating_ge_4_uncond = probability(event_rating_ge_4)

    print("\n2) P(Rating >= 4 | Genre = Comedy)")
    print(f"Conditional: {p_rating_ge_4_given_comedy:.2f}%")
    print(f"Unconditional P(Rating >= 4): {p_rating_ge_4_uncond:.2f}%")

    given_was_rented = ~np.isnan(rental_year)
    event_after_2015 = ~np.isnan(rental_year) & (rental_year > 2015.0)

    p_after_2015_given_rented = conditional_probability(event_after_2015, given_was_rented)
    movie_year_valid = ~np.isnan(movie_year)
    p_after_2015_uncond_movies = (np.count_nonzero(movie_year_valid & (movie_year > 2015.0)) / np.count_nonzero(movie_year_valid)) * 100.0 if np.count_nonzero(movie_year_valid) > 0 else 0.0

    print("\n3) P(Movie released after 2015 | Movie was rented)")
    print(f"Conditional (based on rental rows): {p_after_2015_given_rented:.2f}%")
    print(f"Unconditional (based on movies with year): {p_after_2015_uncond_movies:.2f}%")

    unique_customers_with_rent = np.unique(cust_ids)
    female_mask_rows = cust_gender == "female"

    denom_unique = unique_customers_with_rent.size
    female_customers = np.unique(cust_ids[female_mask_rows])
    p_female_given_rented = (female_customers.size / denom_unique) * 100.0 if denom_unique > 0 else 0.0

    all_customers = fetch_array(cursor, "SELECT customer_id, gender FROM customers")
    all_gender = normalize_text(all_customers[:, 1])
    p_female_uncond = probability(all_gender == "female")

    print("\n4) P(Customer is Female | Customer rented at least one movie)")
    print(f"Conditional (unique customers who rented): {p_female_given_rented:.2f}%")
    print(f"Unconditional P(Female) (all customers): {p_female_uncond:.2f}%")

    given_year_lt_2000 = ~np.isnan(movie_year) & (movie_year < 2000.0)
    event_runtime_gt_120 = ~np.isnan(movie_runtime) & (movie_runtime > 120.0)

    p_runtime_gt_120_given_old = conditional_probability(event_runtime_gt_120, given_year_lt_2000)
    p_runtime_gt_120_uncond = probability(event_runtime_gt_120)

    print("\n5) P(Runtime > 120 | Year of release < 2000)")
    print(f"Conditional: {p_runtime_gt_120_given_old:.2f}%")
    print(f"Unconditional P(Runtime > 120): {p_runtime_gt_120_uncond:.2f}%")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
