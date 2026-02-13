import pandas as pd
from server import get_connection


def fetch_dataframe(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def clean_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


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
        print("No data available for Person 7.")
        cursor.close()
        conn.close()
        return

    numeric_columns = [
        "runtime",
        "year_of_release",
        "renting_price",
        "avg_rating",
        "rating"
    ]

    df = clean_numeric(df, numeric_columns)

    print("\nPERSON 7 — FINAL SUMMARY & REPORTING")

    print("\nCLEANED DATASET PREVIEW")
    print(df.head())

    print("\nFINAL CONCLUSIONS")

    print("1) Rental activity is concentrated in a limited number of genres and titles.")
    print("2) Customer ratings tend to cluster in higher values, suggesting overall positive feedback.")
    print("3) Some numerical columns contain outliers that may influence averages and summary statistics.")
    print("4) Revenue distribution is not evenly spread across categories or countries.")

    print("\nDATA QUALITY IMPROVEMENT SUGGESTIONS")

    print("1) Standardize categorical values (e.g., consistent capitalization for genre, country, gender).")
    print("2) Enforce NOT NULL constraints where appropriate (e.g., runtime, year_of_release).")
    print("3) Validate rating input range (1–5 only) at database level.")
    print("4) Monitor extreme values in renting_price and runtime to prevent data entry errors.")
    print("5) Reduce duplication risk by ensuring proper primary and foreign key constraints.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
