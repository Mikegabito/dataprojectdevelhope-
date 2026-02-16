from server import get_connection


def fetch_data(cursor, query: str):
    cursor.execute(query)
    return cursor.fetchall()


def probability(favorable: int, total: int) -> float:
    """Return P(A) = favorable / total (0 if total=0)."""
    return (favorable / total) if total else 0.0


def pct(p: float, decimals: int = 2) -> str:
    return f"{p * 100:.{decimals}f}%"


def count_by_key(rows, key_index: int):
    """Counts occurrences of rows[*][key_index], skipping None."""
    counts = {}
    for row in rows:
        key = row[key_index]
        if key is None:
            continue
        counts[key] = counts.get(key, 0) + 1
    return counts


def print_prob(title: str, sample_space_desc: str, event_desc: str, favorable: int, total: int):
    p = probability(favorable, total)
    print(f"\n{title}")
    print(f"Sample space (S): {sample_space_desc}  -> |S| = {total}")
    print(f"Event (A): {event_desc}  -> |A| = {favorable}")
    print(f"P(A) = |A| / |S| = {favorable} / {total} = {p:.6f} ({pct(p)})")


def main():
    conn = get_connection()
    cursor = conn.cursor()

    # Pull minimal raw data (SQL only for extraction)
    movies = fetch_data(cursor, "SELECT genre, runtime, year_of_release FROM movies")
    rentings = fetch_data(cursor, "SELECT rating FROM rentings")
    customers = fetch_data(cursor, "SELECT country, gender FROM customers")

    total_movies = len(movies)
    total_rentings = len(rentings)
    total_customers = len(customers)

    # 1) P(movie belongs to each genre)
    print("\n" + "=" * 60)
    print("1) MOVIE GENRE PROBABILITIES")
    print("=" * 60)

    genre_counts = {}
    for genre, _, _ in movies:
        if genre is None:
            continue
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    for genre in sorted(genre_counts):
        favorable = genre_counts[genre]
        print_prob(
            title=f"Genre = {genre}",
            sample_space_desc="All movies",
            event_desc=f"Selected movie has genre '{genre}'",
            favorable=favorable,
            total=total_movies,
        )

    # 2) P(movie released after 2000/2010/2020)
    print("\n" + "=" * 60)
    print("2) MOVIES RELEASED AFTER A YEAR")
    print("=" * 60)

    for year in [2000, 2010, 2020]:
        favorable = sum(1 for _, _, y in movies if y is not None and y > year)
        print_prob(
            title=f"Release year > {year}",
            sample_space_desc="All movies",
            event_desc=f"Movie released after {year}",
            favorable=favorable,
            total=total_movies,
        )

    # 3) P(rented movie has a rating)
    print("\n" + "=" * 60)
    print("3) RENTINGS WITH A RATING (NOT NULL)")
    print("=" * 60)

    rated = [r for (r,) in rentings if r is not None]
    print_prob(
        title="Renting has a rating",
        sample_space_desc="All rentings",
        event_desc="Renting.rating is not NULL",
        favorable=len(rated),
        total=total_rentings,
    )

    # 4) P(rating == k) for k=1..5  (conditioned on 'has a rating')
    print("\n" + "=" * 60)
    print("4) RATING DISTRIBUTION (1–5) AMONG RATED RENTINGS")
    print("=" * 60)

    # Sample space here is ONLY rated rentings (since NULL isn't a 1–5 value)
    total_rated = len(rated)
    rating_counts = {}
    for r in rated:
        rating_counts[r] = rating_counts.get(r, 0) + 1

    for k in range(1, 6):
        favorable = rating_counts.get(k, 0)
        print_prob(
            title=f"Rating = {k}",
            sample_space_desc="All rated rentings (rating NOT NULL)",
            event_desc=f"Rated renting has rating equal to {k}",
            favorable=favorable,
            total=total_rated,
        )

    # 5) P(runtime exceeds 90/120/150)
    print("\n" + "=" * 60)
    print("5) MOVIE RUNTIME THRESHOLDS")
    print("=" * 60)

    for minutes in [90, 120, 150]:
        favorable = sum(1 for _, runtime, _ in movies if runtime is not None and runtime > minutes)
        print_prob(
            title=f"Runtime > {minutes} minutes",
            sample_space_desc="All movies",
            event_desc=f"Movie runtime exceeds {minutes} minutes",
            favorable=favorable,
            total=total_movies,
        )

    # 6) P(customer from each country)
    print("\n" + "=" * 60)
    print("6) CUSTOMER COUNTRY PROBABILITIES")
    print("=" * 60)

    country_counts = {}
    for country, _ in customers:
        if country is None:
            continue
        country_counts[country] = country_counts.get(country, 0) + 1

    for country in sorted(country_counts):
        favorable = country_counts[country]
        print_prob(
            title=f"Country = {country}",
            sample_space_desc="All customers",
            event_desc=f"Customer country is '{country}'",
            favorable=favorable,
            total=total_customers,
        )

    # 7) Gender probability distribution
    print("\n" + "=" * 60)
    print("7) CUSTOMER GENDER PROBABILITIES")
    print("=" * 60)

    gender_counts = {}
    for _, gender in customers:
        if gender is None:
            continue
        gender_counts[gender] = gender_counts.get(gender, 0) + 1

    for gender in sorted(gender_counts):
        favorable = gender_counts[gender]
        print_prob(
            title=f"Gender = {gender}",
            sample_space_desc="All customers",
            event_desc=f"Customer gender is '{gender}'",
            favorable=favorable,
            total=total_customers,
        )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
