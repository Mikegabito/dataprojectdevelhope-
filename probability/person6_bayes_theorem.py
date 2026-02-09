from server import get_connection

def fetch_data(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def percentage(part, total):
    if total == 0:
        return 0
    return (part / total) * 100

def normalize_text(value):
    if value is None:
        return None
    return str(value).strip().lower()

def most_common_non_null(values):
    counts = {}
    for v in values:
        if v is None:
            continue
        counts[v] = counts.get(v, 0) + 1
    if not counts:
        return None
    return max(counts.items(), key=lambda x: x[1])[0]

def bayes_posterior_percent(prior_percent, likelihood_percent, evidence_percent):
    if evidence_percent == 0:
        return 0
    return (prior_percent / 100) * (likelihood_percent / 100) / (evidence_percent / 100) * 100

def print_bayes_block(title, prior, likelihood, evidence, posterior_bayes, posterior_direct):
    diff = abs(posterior_bayes - posterior_direct)
    print(title)
    print(f"Prior: {prior:.2f}%")
    print(f"Likelihood: {likelihood:.2f}%")
    print(f"Evidence: {evidence:.2f}%")
    print(f"Posterior (Bayes): {posterior_bayes:.2f}%")
    print(f"Posterior (Direct check): {posterior_direct:.2f}%")
    print(f"Difference: {diff:.2f}%")
    print("")

def main():
    conn = get_connection()
    cursor = conn.cursor()

    rated_rentings = fetch_data(
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

    if not rated_rentings:
        print("Not enough data to run Person 6 (no rated rentings).")
        cursor.close()
        conn.close()
        return

    rated_genres = [normalize_text(g) for (g, _) in rated_rentings]
    genre_counts = {}
    for g in rated_genres:
        if g is None:
            continue
        genre_counts[g] = genre_counts.get(g, 0) + 1

    preferred_genre = "drama"
    if preferred_genre not in genre_counts:
        preferred_genre = most_common_non_null(rated_genres)

    total_rated = len(rated_rentings)
    total_preferred_genre = sum(1 for (g, _) in rated_rentings if normalize_text(g) == preferred_genre)

    evidence_count = sum(1 for (_, rating) in rated_rentings if rating is not None and rating >= 4)
    evidence_percent = percentage(evidence_count, total_rated)

    prior_percent = percentage(total_preferred_genre, total_rated)

    likelihood_count = sum(
        1 for (g, rating) in rated_rentings
        if normalize_text(g) == preferred_genre and rating is not None and rating >= 4
    )
    likelihood_percent = percentage(likelihood_count, total_preferred_genre)

    posterior_bayes = bayes_posterior_percent(prior_percent, likelihood_percent, evidence_percent)

    direct_numerator = sum(
        1 for (g, rating) in rated_rentings
        if rating is not None and rating >= 4 and normalize_text(g) == preferred_genre
    )
    direct_denominator = sum(
        1 for (_, rating) in rated_rentings
        if rating is not None and rating >= 4
    )
    posterior_direct = percentage(direct_numerator, direct_denominator)

    print_bayes_block(
        f"EXAMPLE 1: P(Genre = '{preferred_genre.title()}' | Rating >= 4) using rated rentings",
        prior_percent,
        likelihood_percent,
        evidence_percent,
        posterior_bayes,
        posterior_direct
    )

    rentings_with_gender_and_genre = fetch_data(
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

    if not rentings_with_gender_and_genre:
        print("Not enough data to run Example 2 (missing gender or genre in rentings).")
        cursor.close()
        conn.close()
        return

    genders = [normalize_text(g) for (g, _) in rentings_with_gender_and_genre]
    chosen_gender = most_common_non_null(genders)

    all_genres = [normalize_text(g) for (_, g) in rentings_with_gender_and_genre]
    genre_counts2 = {}
    for g in all_genres:
        if g is None:
            continue
        genre_counts2[g] = genre_counts2.get(g, 0) + 1

    preferred_genre2 = "action"
    if preferred_genre2 not in genre_counts2:
        preferred_genre2 = most_common_non_null(all_genres)

    total_events = len(rentings_with_gender_and_genre)

    prior_count2 = sum(
        1 for (_, genre) in rentings_with_gender_and_genre
        if normalize_text(genre) == preferred_genre2
    )
    prior_percent2 = percentage(prior_count2, total_events)

    evidence_count2 = sum(
        1 for (gender, _) in rentings_with_gender_and_genre
        if normalize_text(gender) == chosen_gender
    )
    evidence_percent2 = percentage(evidence_count2, total_events)

    likelihood_den2 = prior_count2
    likelihood_num2 = sum(
        1 for (gender, genre) in rentings_with_gender_and_genre
        if normalize_text(genre) == preferred_genre2 and normalize_text(gender) == chosen_gender
    )
    likelihood_percent2 = percentage(likelihood_num2, likelihood_den2)

    posterior_bayes2 = bayes_posterior_percent(prior_percent2, likelihood_percent2, evidence_percent2)

    direct_num2 = sum(
        1 for (gender, genre) in rentings_with_gender_and_genre
        if normalize_text(gender) == chosen_gender and normalize_text(genre) == preferred_genre2
    )
    direct_den2 = sum(
        1 for (gender, _) in rentings_with_gender_and_genre
        if normalize_text(gender) == chosen_gender
    )
    posterior_direct2 = percentage(direct_num2, direct_den2)

    gender_label = chosen_gender.title() if chosen_gender is not None else "Unknown"
    print_bayes_block(
        f"EXAMPLE 2: P(Genre = '{preferred_genre2.title()}' | Customer gender = '{gender_label}') using rentings",
        prior_percent2,
        likelihood_percent2,
        evidence_percent2,
        posterior_bayes2,
        posterior_direct2
    )

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
