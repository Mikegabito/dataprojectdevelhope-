import pandas as pd
from server import get_connection


def fetch_dataframe(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def main():
    conn = get_connection()
    cursor = conn.cursor()

    df = fetch_dataframe(
        cursor,
        """
        SELECT
            m.movie_id,
            m.title,
            m.genre,
            m.runtime,
            m.year_of_release,
            m.renting_price,
            m.avg_rating,
            r.rating,
            c.country,
            c.gender
        FROM movies m
        LEFT JOIN rentings r
            ON r.movie_id = m.movie_id
        LEFT JOIN customers c
            ON c.customer_id = r.customer_id
        """
    )

    if df.empty:
        print("No data available for Person 4.")
        cursor.close()
        conn.close()
        return

    print("\nPERSON 4 — FILTERING & SORTING")

    filtered_1 = df[
        (df["genre"] == "Drama") &
        (df["avg_rating"] >= 4.0) &
        (df["year_of_release"] > 2010)
    ]

    sorted_1 = filtered_1.sort_values(
        by=["avg_rating", "year_of_release"],
        ascending=[False, False]
    )

    print("\n1) Drama movies (rating >= 4 and released after 2010)")
    print(sorted_1[[
        "title",
        "genre",
        "avg_rating",
        "year_of_release"
    ]].drop_duplicates())

    filtered_2 = df[
        (df["country"] == "Italy") &
        (df["rating"] >= 4)
    ]

    sorted_2 = filtered_2.sort_values(
        by=["rating", "renting_price"],
        ascending=[False, True]
    )

    print("\n2) Rentals from Italy with rating >= 4")
    print(sorted_2[[
        "title",
        "country",
        "rating",
        "renting_price"
    ]])

    filtered_3 = df[
        (df["runtime"] > 120) &
        (df["avg_rating"] >= 3.5)
    ]

    sorted_3 = filtered_3.sort_values(
        by=["runtime", "avg_rating"],
        ascending=[False, False]
    )

    print("\n3) Long movies (runtime > 120) with rating >= 3.5")
    print(sorted_3[[
        "title",
        "runtime",
        "avg_rating"
    ]].drop_duplicates())

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
