from server import get_connection

def fetch_data(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def percentage(part, total):
    if total == 0:
        return 0
    return (part / total) * 100

def most_common_non_null(values):
    counts = {}
    for v in values:
        if v is None:
            continue
        counts[v] = counts.get(v, 0) + 1
    if not counts:
        return None
    return max(counts.items(), key=lambda x: x[1])[0]

def independence_report(title, p_a, p_b, p_a_and_b, tolerance_pct=1.0):
    product = (p_a / 100) * (p_b / 100) * 100
    diff = abs(p_a_and_b - product)

    print(title)
    print(f"P(A): {p_a:.2f}%")
    print(f"P(B): {p_b:.2f}%")
    print(f"P(A and B): {p_a_and_b:.2f}%")
    print(f"P(A) x P(B): {product:.2f}%")
    print(f"Difference: {diff:.2f}%")

    if diff <= tolerance_pct:
        print(f"Conclusion: Approximately independent (tolerance {tolerance_pct:.2f}%)")
    else:
        print(f"Conclusion: Likely dependent (difference larger than {tolerance_pct:.2f}%)")
    print("")

def main():
    conn = get_connection()
    cursor = conn.cursor()

    rentings_with_movie = fetch_data(
        cursor,
        """
        SELECT
            m.genre,
            r.rating
        FROM rentings r
        JOIN movies m
            ON m.movie_id = r.movie_id
        WHERE r.rating IS NOT NULL
        """
    )

    all_genres = [g for (g, _) in rentings_with_movie]
    chosen_genre = most_common_non_null(all_genres)

    total = len(rentings_with_movie)
    if total == 0 or chosen_genre is None:
        print("Not enough data to run Person 3 (no rated rentings or missing genres).")
        cursor.close()
        conn.close()
        return

    a_count = 0
    b_count = 0
    a_and_b_count = 0

    for genre, rating in rentings_with_movie:
        is_a = (genre == chosen_genre)
        is_b = (rating is not None and rating >= 4)

        if is_a:
            a_count += 1
        if is_b:
            b_count += 1
        if is_a and is_b:
            a_and_b_count += 1

    p_a = percentage(a_count, total)
    p_b = percentage(b_count, total)
    p_a_and_b = percentage(a_and_b_count, total)

    independence_report(
        f"EXPERIMENT 1: A = Genre is '{chosen_genre}' | B = Rating is 4 or higher (sample: rated rentings)",
        p_a,
        p_b,
        p_a_and_b,
        tolerance_pct=1.0
    )

    customer_renting_gender = fetch_data(
        cursor,
        """
        SELECT
            c.gender,
            r.renting_id
        FROM rentings r
        JOIN customers c
            ON c.customer_id = r.customer_id
        WHERE c.gender IS NOT NULL
        """
    )

    if not customer_renting_gender:
        print("Not enough data to run Experiment 2 (no customer gender data linked to rentings).")
        cursor.close()
        conn.close()
        return

    genders = [g for (g, _) in customer_renting_gender]
    chosen_gender = most_common_non_null(genders)
    if chosen_gender is None:
        print("Not enough data to run Experiment 2 (missing gender values).")
        cursor.close()
        conn.close()
        return

    customer_rent_count = {}
    customer_gender = {}

    customers_full = fetch_data(
        cursor,
        """
        SELECT
            r.customer_id,
            c.gender
        FROM rentings r
        JOIN customers c
            ON c.customer_id = r.customer_id
        WHERE c.gender IS NOT NULL
        """
    )

    for customer_id, gender in customers_full:
        customer_gender[customer_id] = gender
        customer_rent_count[customer_id] = customer_rent_count.get(customer_id, 0) + 1

    customer_ids = list(customer_rent_count.keys())
    total_customers = len(customer_ids)

    a2_count = 0
    b2_count = 0
    a2_and_b2_count = 0

    for cid in customer_ids:
        gender = customer_gender.get(cid)
        rents = customer_rent_count.get(cid, 0)

        is_a2 = (gender == chosen_gender)
        is_b2 = (rents >= 2)

        if is_a2:
            a2_count += 1
        if is_b2:
            b2_count += 1
        if is_a2 and is_b2:
            a2_and_b2_count += 1

    p_a2 = percentage(a2_count, total_customers)
    p_b2 = percentage(b2_count, total_customers)
    p_a2_and_b2 = percentage(a2_and_b2_count, total_customers)

    independence_report(
        f"EXPERIMENT 2: A = Customer gender is '{chosen_gender}' | B = Customer rented 2+ movies (sample: customers who rented)",
        p_a2,
        p_b2,
        p_a2_and_b2,
        tolerance_pct=1.0
    )

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
