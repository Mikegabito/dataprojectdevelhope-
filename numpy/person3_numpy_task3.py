import numpy as np
from server import get_connection

def fetch_array(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return np.array(rows, dtype=object)

def show_info(name, arr):
    print(f"{name} shape: {arr.shape} dtype: {arr.dtype}")

def prob(mask):
    mask = np.asarray(mask, dtype=bool)
    n = mask.size
    if n == 0:
        return 0.0
    return np.count_nonzero(mask) / n

def main():
    conn = get_connection()
    cursor = conn.cursor()

    data = fetch_array(
        cursor,
        """
        SELECT
            m.genre,
            m.runtime,
            r.rating,
            c.gender
        FROM rentings r
        JOIN movies m
            ON m.movie_id = r.movie_id
        JOIN customers c
            ON c.customer_id = r.customer_id
        """
    )

    if data.size == 0:
        print("Not enough data to run Task 3 (no rows returned).")
        cursor.close()
        conn.close()
        return

    genre = np.char.lower(data[:, 0].astype(str))
    runtime_obj = data[:, 1]
    rating_obj = data[:, 2]
    gender = np.char.lower(data[:, 3].astype(str))

    runtime = np.where(runtime_obj == None, np.nan, runtime_obj).astype(float)
    rating = np.where(rating_obj == None, np.nan, rating_obj).astype(float)

    show_info("data", data)
    show_info("genre", genre)
    show_info("runtime", runtime)
    show_info("rating", rating)
    show_info("gender", gender)

    tol = 0.01

    valid_rating = ~np.isnan(rating)
    valid_runtime = ~np.isnan(runtime)

    A1 = (genre == "action")
    B1 = valid_rating & (rating >= 4)

    A2 = valid_runtime & (runtime >= 150)
    B2 = (genre == "drama")

    rated = valid_rating
    A_dep = rated & (rating >= 4)
    B_dep = rated & (rating >= 3)

    pairs = [
        ("Pair 1", "A=Genre is Action", "B=Rating >= 4 (rated only)", A1, B1),
        ("Pair 2", "A=Runtime >= 150", "B=Genre is Drama", A2, B2),
        ("Pair 3", "A=Rating >= 4", "B=Rating >= 3 (clearly dependent)", A_dep, B_dep),
    ]

    headers = ["Pair", "P(A)%", "P(B)%", "P(A∩B)%", "P(A)×P(B)%", "Independent?"]
    print("\nINDEPENDENCE TEST RESULTS")
    print("{:<6} {:>10} {:>10} {:>12} {:>14} {:>14}".format(*headers))

    for pair_name, a_label, b_label, A, B in pairs:
        pA = prob(A)
        pB = prob(B)
        pAB = prob(A & B)
        product = pA * pB
        diff = abs(pAB - product)
        independent = "approx yes" if diff <= tol else "no"

        print("{:<6} {:>10.2f} {:>10.2f} {:>12.2f} {:>14.2f} {:>14}".format(
            pair_name,
            pA * 100,
            pB * 100,
            pAB * 100,
            product * 100,
            independent
        ))

        print(f"  {a_label}")
        print(f"  {b_label}")

    print("")
    print(f"Tolerance used: {tol:.2f}% as a probability difference threshold.")
    print("Pair 3 is designed to be dependent because every rating >= 4 is also >= 3.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

