import numpy as np
import matplotlib.pyplot as plt
from server import get_connection

def fetch_array(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return np.array(rows)

def show_info(name, arr):
    print(f"{name} shape: {arr.shape} dtype: {arr.dtype}")

def estimate_prob_rating_ge_4(ratings, sample_size, rng):
    idx = rng.integers(0, ratings.size, size=sample_size)
    sample = ratings[idx]
    return np.mean(sample >= 4)

def main():
    conn = get_connection()
    cursor = conn.cursor()

    data = fetch_array(
        cursor,
        """
        SELECT rating
        FROM rentings
        WHERE rating IS NOT NULL
        """
    )

    ratings = data[:, 0].astype(float)

    show_info("data", data)
    show_info("ratings", ratings)

    if ratings.size == 0:
        print("Not enough data to run Task 7 (no ratings).")
        cursor.close()
        conn.close()
        return

    rng = np.random.default_rng()

    sizes = np.array([100, 500, 1000, 5000, 10000, 50000, 100000], dtype=int)
    estimates = np.array([estimate_prob_rating_ge_4(ratings, int(s), rng) for s in sizes], dtype=float)

    exact = np.mean(ratings >= 4)

    print("\nEXPERIMENT: Probability that rating is 4 or higher")
    for s, est in zip(sizes, estimates):
        print(f"Sample size {int(s)} -> estimate: {est*100:.2f}%")

    print(f"\nExact (from full rated data): {exact*100:.2f}%")

    plt.figure()
    plt.plot(sizes, estimates * 100)
    plt.axhline(exact * 100)
    plt.xscale("log")
    plt.xlabel("Sample size (log scale)")
    plt.ylabel("Estimated probability (%)")
    plt.title("Convergence of P(rating >= 4) with increasing sample sizes")
    plt.show()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
