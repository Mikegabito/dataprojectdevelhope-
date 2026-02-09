from server import get_connection

def fetch_data(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def percentage(part, total):
    if total == 0:
        return 0
    return (part / total) * 100

def main():
    conn = get_connection()
    cursor = conn.cursor()

    movies = fetch_data(
        cursor,
        "SELECT genre, runtime, year_of_release FROM movies"
    )

    rentings = fetch_data(
        cursor,
        "SELECT rating FROM rentings"
    )

    customers = fetch_data(
        cursor,
        "SELECT country, gender FROM customers"
    )

    total_movies = len(movies)
    total_rentings = len(rentings)
    total_customers = len(customers)

    print("MOVIE GENRE PROBABILITY")
    genres = {}
    for genre, _, _ in movies:
        genres[genre] = genres.get(genre, 0) + 1

    for genre, count in genres.items():
        print(f"{genre}: {percentage(count, total_movies):.2f}%")

    print("\nMOVIES RELEASED AFTER YEAR")
    for year in [2000, 2010, 2020]:
        count = sum(1 for _, _, y in movies if y and y > year)
        print(f"After {year}: {percentage(count, total_movies):.2f}%")

    print("\nMOVIE RUNTIME PROBABILITY")
    for minutes in [90, 120, 150]:
        count = sum(1 for _, r, _ in movies if r and r > minutes)
        print(f"Longer than {minutes} minutes: {percentage(count, total_movies):.2f}%")

    print("\nRENTING RATING PROBABILITY")
    rated = [r for (r,) in rentings if r is not None]
    print(f"Rentings with rating: {percentage(len(rated), total_rentings):.2f}%")

    rating_counts = {}
    for r in rated:
        rating_counts[r] = rating_counts.get(r, 0) + 1

    for rating in sorted(rating_counts):
        print(f"Rating {rating}: {percentage(rating_counts[rating], len(rated)):.2f}%")

    print("\nCUSTOMER COUNTRY PROBABILITY")
    countries = {}
    for country, _ in customers:
        countries[country] = countries.get(country, 0) + 1

    for country, count in countries.items():
        print(f"{country}: {percentage(count, total_customers):.2f}%")

    print("\nCUSTOMER GENDER PROBABILITY")
    genders = {}
    for _, gender in customers:
        genders[gender] = genders.get(gender, 0) + 1

    for gender, count in genders.items():
        print(f"{gender}: {percentage(count, total_customers):.2f}%")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
