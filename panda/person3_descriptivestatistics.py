import numpy as np
import pandas as pd
from server import get_connection


def fetch_dataframe(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def manual_mean(arr):
    arr = arr[~np.isnan(arr)]
    return np.sum(arr) / arr.size if arr.size > 0 else np.nan


def manual_median(arr):
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        return np.nan
    arr_sorted = np.sort(arr)
    n = arr_sorted.size
    mid = n // 2
    if n % 2 == 0:
        return (arr_sorted[mid - 1] + arr_sorted[mid]) / 2
    return arr_sorted[mid]


def manual_mode(arr):
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        return np.nan
    values, counts = np.unique(arr, return_counts=True)
    return values[np.argmax(counts)]


def main():
    conn = get_connection()
    cursor = conn.cursor()

    df = fetch_dataframe(
        cursor,
        """
        SELECT
            m.runtime,
            m.year_of_release,
            m.renting_price,
            m.avg_rating,
            r.rating
        FROM movies m
        LEFT JOIN rentings r
            ON r.movie_id = m.movie_id
        """
    )

    if df.empty:
        print("No data available for Person 3.")
        cursor.close()
        conn.close()
        return

    print("\nPERSON 3 — DESCRIPTIVE STATISTICS")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    print("\nDESCRIBE() OUTPUT")
    print(df[numeric_cols].describe())

    for col in numeric_cols:
        arr = df[col].astype(float).to_numpy()

        print(f"\nCOLUMN: {col}")

        print(f"Mean (manual): {manual_mean(arr):.2f}")
        print(f"Median (manual): {manual_median(arr):.2f}")
        print(f"Mode (manual): {manual_mode(arr):.2f}")

        arr_clean = arr[~np.isnan(arr)]

        if arr_clean.size > 0:
            print(f"Min: {np.min(arr_clean):.2f}")
            print(f"Max: {np.max(arr_clean):.2f}")
            print(f"Std Dev: {np.std(arr_clean, ddof=1):.2f}")
        else:
            print("Min: N/A")
            print("Max: N/A")
            print("Std Dev: N/A")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
