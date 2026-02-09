from __future__ import annotations

from server import format_probability

import random
from typing import Dict, List, Optional, Tuple

from server import get_connection

# -----------------------------
# Optional visualization (Bonus)
# -----------------------------

def _try_import_matplotlib():
    try:
        import matplotlib.pyplot as plt  
        return plt
    except Exception:
        return None

# -----------------------------
# Raw data extraction (SQL allowed only here)
# -----------------------------

def load_rentings_data() -> Tuple[List[Optional[int]], List[int]]:

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT rating, customer_id FROM public.rentings;")
            rows = cur.fetchall()

        ratings: List[Optional[int]] = []
        customer_ids: List[int] = []
        for rating, customer_id in rows:
            ratings.append(rating)         # None if NULL
            customer_ids.append(customer_id)

        return ratings, customer_ids
    finally:
        conn.close()

# -----------------------------
# Exact probabilities (empirical baseline from DB)
# -----------------------------

def exact_probability_rating_geq_k(ratings: List[Optional[int]], k: int = 4) -> Tuple[float, int, int]:

    rated = [r for r in ratings if r is not None]
    total_rated = len(rated)
    if total_rated == 0:
        return 0.0, 0, 0

    favorable = sum(1 for r in rated if r >= k)
    return favorable / total_rated, favorable, total_rated

def rentals_per_customer(customer_ids: List[int]) -> Dict[int, int]:

    counts: Dict[int, int] = {}
    for cid in customer_ids:
        counts[cid] = counts.get(cid, 0) + 1
    return counts

def exact_probability_customer_rents_geq_2(customer_ids: List[int]) -> Tuple[float, int, int]:

    counts = rentals_per_customer(customer_ids)
    total_customers = len(counts)
    if total_customers == 0:
        return 0.0, 0, 0

    favorable = sum(1 for v in counts.values() if v >= 2)
    return favorable / total_customers, favorable, total_customers

# -----------------------------
# Monte Carlo simulations 
# -----------------------------

def simulate_rating_geq_k(
    ratings: List[Optional[int]],
    n_trials: int = 10_000,
    k: int = 4,
    seed: Optional[int] = 42
) -> Tuple[float, int, int]:

    if seed is not None:
        random.seed(seed)

    favorable_sim = 0
    total_rated_sim = 0

    for _ in range(n_trials):
        r = random.choice(ratings)
        if r is None:
            continue
        total_rated_sim += 1
        if r >= k:
            favorable_sim += 1

    p_hat = favorable_sim / total_rated_sim if total_rated_sim else 0.0
    return p_hat, favorable_sim, total_rated_sim

def simulate_customer_rents_geq_2(
    customer_ids: List[int],
    n_trials: int = 10_000,
    seed: Optional[int] = 42
) -> Tuple[float, int, int]:

    if seed is not None:
        random.seed(seed)

    counts = rentals_per_customer(customer_ids)
    customers = list(counts.keys())
    if not customers:
        return 0.0, 0, 0

    favorable = 0
    for _ in range(n_trials):
        c = random.choice(customers)
        if counts[c] >= 2:
            favorable += 1

    return favorable / n_trials, favorable, n_trials

# -----------------------------
# Convergence + LLN
# -----------------------------

def convergence_study(
    ratings: List[Optional[int]],
    k: int = 4,
    sizes: Optional[List[int]] = None
) -> List[Tuple[int, float]]:

    if sizes is None:
        sizes = [100, 500, 1_000, 5_000, 10_000, 50_000]

    results: List[Tuple[int, float]] = []
    for n in sizes:
        p_hat, _, _ = simulate_rating_geq_k(ratings, n_trials=n, k=k, seed=42)
        results.append((n, p_hat))
    return results

def explain_lln(exact_p: float, conv: List[Tuple[int, float]]) -> None:

    print("\nLaw of Large Numbers (LLN):")
    print("- As the number of simulations n increases, the simulated proportion p̂ tends to get closer to the true probability.")
    print(f"- Here the true (empirical exact) probability from the full database is: "f"{format_probability(exact_p)}")
    if conv:
        first_n, first_p = conv[0]
        last_n, last_p = conv[-1]
        print(f"- Example: at n={first_n}, p̂={format_probability(first_p)}; at n={last_n}, p̂={format_probability(last_p)}")
    print("- Small n usually fluctuates more; large n usually stabilizes.")

# -----------------------------
# Visualization (Bonus)
# -----------------------------

def plot_convergence(conv: List[Tuple[int, float]], exact_p: float) -> None:

    plt = _try_import_matplotlib()
    if plt is None:
        print("\nMatplotlib is not installed (or failed to import).")
        print("Install it with: pip install matplotlib")
        return

    sizes = [n for n, _ in conv]
    estimates = [p for _, p in conv]

    plt.figure(figsize=(9, 5))
    plt.plot(sizes, estimates, marker="o", label="Simulated p̂")
    plt.axhline(y=exact_p, linestyle="--", label="Exact p")
    plt.xlabel("Number of simulations (n)")
    plt.ylabel("Estimated probability P(rating ≥ 4)")
    plt.title("Monte Carlo Convergence (Law of Large Numbers)")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_cumulative_rating_probability(ratings: List[Optional[int]]) -> None:

    plt = _try_import_matplotlib()
    if plt is None:
        print("\nMatplotlib is not installed.")
        print("Install it with: pip install matplotlib")
        return

    rated = [r for r in ratings if r is not None]
    if not rated:
        print("\nNo non-null ratings available to plot.")
        return

    total = len(rated)
    unique_ratings = sorted(set(rated))

    cumulative_probs = []
    for x in unique_ratings:
        count = sum(1 for r in rated if r >= x)
        cumulative_probs.append(count / total)

    plt.figure(figsize=(9, 5))
    plt.plot(unique_ratings, cumulative_probs, marker="o")
    plt.xlabel("Rating threshold (x)")
    plt.ylabel("P(Rating ≥ x)")
    plt.title("Cumulative Probability of Movie Ratings")
    plt.grid(True)
    plt.show()


# -----------------------------
# Menu
# -----------------------------

def print_menu() -> None:
    print("\n=== – Monte Carlo Simulation ===")
    print("1) Load data from Supabase (rentings)")
    print("2) Simulate 10,000 random rentals → estimate P(rating ≥ 4)")
    print("3) Compare simulated vs exact probability (rating ≥ 4)")
    print("4) Simulate customer behavior → P(customer rents ≥ 2)")
    print("5) Convergence study + LLN explanation (rating ≥ 4)")
    print("6) Plot convergence (Matplotlib)")
    print("7) Plot cumulative rating probability P(rating ≥ x)")
    print("0) Exit")

def main() -> None:
    ratings: List[Optional[int]] = []
    customer_ids: List[int] = []

    last_sim_rating: Optional[Tuple[float, int, int]] = None  
    last_conv: Optional[List[Tuple[int, float]]] = None
    last_exact_p: Optional[float] = None

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Bye!")
            break

        elif choice == "1":
            ratings, customer_ids = load_rentings_data()
            print(f"\nLoaded rentals: {len(ratings)} rows")
            null_count = sum(1 for r in ratings if r is None)
            print(f"NULL ratings: {null_count}")
            if ratings:
                print(f"First 5 ratings: {ratings[:5]}")
                print(f"First 5 customer_ids: {customer_ids[:5]}")

        elif choice == "2":
            if not ratings:
                print("\nLoad data first (option 1).")
                continue
            p_hat, fav, total_rated_sim = simulate_rating_geq_k(ratings, n_trials=10_000, k=4, seed=42)
            last_sim_rating = (p_hat, fav, total_rated_sim)
            print("\nSimulation (10,000 random rentals):")
            print(f"Estimated P(rating ≥ 4 | rating exists) = "f"{format_probability(p_hat)} = {fav}/{total_rated_sim}")

        elif choice == "3":
            if not ratings:
                print("\nLoad data first (option 1).")
                continue

            exact_p, efav, etotal = exact_probability_rating_geq_k(ratings, k=4)
            last_exact_p = exact_p

            print("\nCompare simulated vs exact (rating ≥ 4):")
            print("Definition:")
            print("  P(R ≥ 4 | rating exists) = (# rated rentals with rating ≥ 4) / (# rentals with rating not NULL)")
            print(f"Exact (from DB): {format_probability(exact_p)} = {efav}/{etotal}")

            if last_sim_rating is None:
                print("Simulated: run option 2 first.")
            else:
                p_hat, fav, total_rated_sim = last_sim_rating
                print(f"Simulated (last run): {format_probability(p_hat)} = {fav}/{total_rated_sim}")

        elif choice == "4":
            if not customer_ids:
                print("\nLoad data first (option 1).")
                continue

            sim_p, sim_fav, n = simulate_customer_rents_geq_2(customer_ids, n_trials=10_000, seed=42)
            exact_p, efav, etotal = exact_probability_customer_rents_geq_2(customer_ids)

            print("\nCustomer behavior: P(customer rents ≥ 2 movies)")
            print("Definition:")
            print("  P(Y ≥ 2) = (# customers with ≥ 2 rentals) / (# customers who rented at least once)")
            print(f"Simulated (10,000):{format_probability(sim_p)} = {sim_fav}/{n}")
            print(f"Exact (from DB):{format_probability(exact_p)} = {efav}/{etotal}")


        elif choice == "5":
            if not ratings:
                print("\nLoad data first (option 1).")
                continue

            exact_p, _, _ = exact_probability_rating_geq_k(ratings, k=4)
            conv = convergence_study(ratings, k=4, sizes=[100, 500, 1_000, 5_000, 10_000, 50_000])

            last_exact_p = exact_p
            last_conv = conv

            print("\nConvergence study for P(rating ≥ 4 | rating exists):")
            for n, p_hat in conv:
                (f"n={n:<6}  p̂={format_probability(p_hat)}")

            explain_lln(exact_p, conv)

        elif choice == "6":
            if not last_conv or last_exact_p is None:
                print("\nRun option 5 first to generate convergence results.")
                continue
            plot_convergence(last_conv, last_exact_p)

        elif choice == "7":
            if not ratings:
               print("\nLoad data first (option 1).")
               continue
            plot_cumulative_rating_probability(ratings)

        else:
            print("\nInvalid option. Try again.")

if __name__ == "__main__":
    main()
