import numpy as np
from server import get_connection

def fetch_array(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return np.array(rows)

def show_info(name, arr):
    print(f"{name} shape: {arr.shape} dtype: {arr.dtype}")

def safe_div(a, b):
    return a / b if b != 0 else 0.0

def main():
    conn = get_connection()
    cursor = conn.cursor()

    data1 = fetch_array(
        cursor,
        """
        SELECT
            m.genre,
            r.rating
        FROM rentings r
        JOIN movies m
            ON m.movie_id = r.movie_id
        WHERE r.rating IS NOT NULL
          AND m.genre IS NOT NULL
        """
    )

    genre1 = np.char.lower(data1[:, 0].astype(str))
    rating1 = data1[:, 1].astype(float)

    show_info("data1", data1)
    show_info("genre1", genre1)
    show_info("rating1", rating1)

    target_genre = "drama"
    if np.count_nonzero(genre1 == target_genre) == 0:
        unique, counts = np.unique(genre1, return_counts=True)
        target_genre = unique[np.argmax(counts)]

    A = (genre1 == target_genre)
    B = (rating1 >= 4)

    prior = safe_div(np.count_nonzero(A), A.size)
    likelihood = safe_div(np.count_nonzero(A & B), np.count_nonzero(A))
    evidence = safe_div(np.count_nonzero(B), B.size)

    posterior = safe_div(likelihood * prior, evidence)

    direct = safe_div(np.count_nonzero(A & B), np.count_nonzero(B))

    print(f"\nEXAMPLE 1: P(Genre={target_genre.title()} | Rating>=4)")
    print(f"Prior P(Genre): {prior*100:.2f}%")
    print(f"Likelihood P(Rating>=4 | Genre): {likelihood*100:.2f}%")
    print(f"Evidence P(Rating>=4): {evidence*100:.2f}%")
    print(f"Posterior (Bayes): {posterior*100:.2f}%")
    print(f"Posterior (Direct check): {direct*100:.2f}%")

    data2 = fetch_array(
        cursor,
        """
        SELECT
            c.gender,
            m.genre
        FROM rentings r
        JOIN customers c
            ON c.customer_id = r.customer_id
        JOIN movies m
            ON m.movie_id = r.movie_id
        WHERE c.gender IS NOT NULL
          AND m.genre IS NOT NULL
        """
    )

    gender2 = np.char.lower(data2[:, 0].astype(str))
    genre2 = np.char.lower(data2[:, 1].astype(str))

    show_info("data2", data2)
    show_info("gender2", gender2)
    show_info("genre2", genre2)

    male = np.count_nonzero(gender2 == "male")
    female = np.count_nonzero(gender2 == "female")
    target_gender = "male" if male >= female else "female"

    target_genre2 = "action"
    if np.count_nonzero(genre2 == target_genre2) == 0:
        unique2, counts2 = np.unique(genre2, return_counts=True)
        target_genre2 = unique2[np.argmax(counts2)]

    A2 = (genre2 == target_genre2)
    B2 = (gender2 == target_gender)

    prior2 = safe_div(np.count_nonzero(A2), A2.size)
    likelihood2 = safe_div(np.count_nonzero(A2 & B2), np.count_nonzero(A2))
    evidence2 = safe_div(np.count_nonzero(B2), B2.size)

    posterior2 = safe_div(likelihood2 * prior2, evidence2)
    direct2 = safe_div(np.count_nonzero(A2 & B2), np.count_nonzero(B2))

    print(f"\nEXAMPLE 2: P(Genre={target_genre2.title()} | Gender={target_gender.title()})")
    print(f"Prior P(Genre): {prior2*100:.2f}%")
    print(f"Likelihood P(Gender | Genre): {likelihood2*100:.2f}%")
    print(f"Evidence P(Gender): {evidence2*100:.2f}%")
    print(f"Posterior (Bayes): {posterior2*100:.2f}%")
    print(f"Posterior (Direct check): {direct2*100:.2f}%")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
