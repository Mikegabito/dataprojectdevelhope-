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
            m.genre,
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
        print("No data available for Person 5.")
        cursor.close()
        conn.close()
        return

    print("\nPERSON 5 — GROUPBY & AGGREGATION")

    print("\n1) Group by Genre")
    group_genre = df.groupby("genre").agg(
        total_rentals=("rating", "count"),
        avg_movie_rating=("avg_rating", "mean"),
        total_revenue=("renting_price", "sum")
    ).sort_values(by="total_rentals", ascending=False)

    print(group_genre)

    print("\n2) Group by Country")
    group_country = df.groupby("country").agg(
        total_rentals=("rating", "count"),
        avg_customer_rating=("rating", "mean"),
        total_revenue=("renting_price", "sum")
    ).sort_values(by="total_revenue", ascending=False)

    print(group_country)

    print("\n3) Group by Gender")
    group_gender = df.groupby("gender").agg(
        total_rentals=("rating", "count"),
        avg_customer_rating=("rating", "mean"),
        total_revenue=("renting_price", "sum")
    ).sort_values(by="total_rentals", ascending=False)

    print(group_gender)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
