import pandas as pd
import numpy as np
from server import get_connection


def fetch_dataframe(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def as_float_series(series):
    return pd.to_numeric(series, errors="coerce").astype(float)


def detect_outliers_iqr(series):
    s = as_float_series(series).dropna()
    if s.empty:
        return pd.Series(dtype=float)
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return s[(s < lower) | (s > upper)]


def main():
    conn = get_connection()
    cursor = conn.cursor()

    df = fetch_dataframe(
        cursor,
        """
        SELECT
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
        print("No data available for Person 6.")
        cursor.close()
        conn.close()
        return

    print("\nPERSON 6 — EDA INSIGHTS")

    print("\nOUTLIER DETECTION (IQR METHOD)")

    for col in ["runtime", "renting_price", "avg_rating", "rating", "year_of_release"]:
        if col in df.columns:
            outliers = detect_outliers_iqr(df[col])
            print(f"\nColumn: {col}")
            print(f"Number of outliers: {len(outliers)}")
            if not outliers.empty:
                print(outliers.head())

    print("\nVALUE COUNTS — GENRE (Top 5)")
    print(df["genre"].astype(str).value_counts().head(5))

    print("\nVALUE COUNTS — COUNTRY (Top 5)")
    print(df["country"].astype(str).value_counts().head(5))

    print("\nVALUE COUNTS — TITLE (Top 5 Most Frequent)")
    print(df["title"].astype(str).value_counts().head(5))

    print("\nEDA INSIGHTS")
    print("1) Some numeric columns include extreme values compared to the majority (outliers), which can influence averages.")
    print("2) Genre frequency is concentrated: a few genres appear much more often than others.")
    print("3) A small set of titles appears very frequently, meaning rentals are not evenly distributed across the catalog.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
