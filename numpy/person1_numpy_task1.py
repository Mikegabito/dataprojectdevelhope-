import numpy as np
from server import get_connection

def fetch_array(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return np.array(rows, dtype=object)

def show_info(name, arr):
    print(f"{name} shape: {arr.shape} dtype: {arr.dtype}")

def main():
    conn = get_connection()
    cursor = conn.cursor()

    data = fetch_array(
        cursor,
        """
        SELECT
            m.runtime,
            m.genre,
            r.rating
        FROM rentings r
        JOIN movies m
            ON m.movie_id = r.movie_id
        """
    )

    if data.size == 0:
        print("Not enough data to run Task 1 (no rows returned).")
        cursor.close()
        conn.close()
        return

    runtime_obj = data[:, 0]
    genre = data[:, 1].astype(str)
    rating_obj = data[:, 2]

    runtime = np.where(runtime_obj == None, np.nan, runtime_obj).astype(float)
    rating = np.where(rating_obj == None, np.nan, rating_obj).astype(float)

    show_info("data", data)
    show_info("runtime", runtime)
    show_info("genre", genre)
    show_info("rating", rating)

    valid_runtime = ~np.isnan(runtime)
    denom = np.count_nonzero(valid_runtime)

    c1 = valid_runtime & (runtime < 80)
    c2 = valid_runtime & (runtime >= 80) & (runtime < 100)
    c3 = valid_runtime & (runtime >= 100) & (runtime < 120)
    c4 = valid_runtime & (runtime >= 120) & (runtime < 150)
    c5 = valid_runtime & (runtime >= 150)

    print("\nRUNTIME CATEGORY PROBABILITIES (based on available runtime values)")
    print(f"Denominator count (valid runtime): {int(denom)}")

    categories = [
        ("< 80 min", c1),
        ("80-99 min", c2),
        ("100-119 min", c3),
        ("120-149 min", c4),
        (">= 150 min", c5),
    ]

    for label, mask in categories:
        prob = (np.count_nonzero(mask) / denom) * 100.0 if denom > 0 else 0.0
        print(f"{label}: {prob:.2f}%")

    manual_count = np.count_nonzero(c3)
    manual_prob = (manual_count / denom) * 100.0 if denom > 0 else 0.0

    func_prob = (np.count_nonzero(c3[valid_runtime]) / denom) * 100.0 if denom > 0 else 0.0

    print("\nMANUAL VERIFICATION (category 100-119 min)")
    print(f"Count in category: {int(manual_count)}")
    print(f"Manual probability: {manual_prob:.2f}%")
    print(f"Vectorized probability: {func_prob:.2f}%")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
