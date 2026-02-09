from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


from server import get_connection, format_probability


# -----------------------------
# Raw data extraction ONLY
# -----------------------------

def load_ratings_and_customers() -> Tuple[np.ndarray, np.ndarray]:
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT rating, customer_id FROM public.rentings;")
            rows = cur.fetchall()
    finally:
        conn.close()

    ratings_obj = np.array([r[0] for r in rows], dtype=object)
    customer_ids = np.array([r[1] for r in rows], dtype=np.int32)

    return ratings_obj, customer_ids


# -----------------------------
# Theoretical results (empirical exact from DB)
# -----------------------------

def theoretical_p_rating_ge_4(ratings_obj: np.ndarray) -> Tuple[float, np.ndarray]:

    mask = ratings_obj != None  # object array safe check
    rated = ratings_obj[mask].astype(np.int16)  # compact
    p_exact = np.mean(rated >= 4)  # NumPy numeric work
    return float(p_exact), rated


def theoretical_p_customer_ge_2(customer_ids: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray]:

    unique_customers, counts = np.unique(customer_ids, return_counts=True)
    p_exact = np.mean(counts >= 2)
    return float(p_exact), unique_customers.astype(np.int32), counts.astype(np.int32)


# -----------------------------
# Monte Carlo (>=500,000) using NumPy RNG
# -----------------------------

def simulate_rating_ge_4(rated_ratings: np.ndarray, n: int = 500_000, seed: int = 42) -> Tuple[float, np.ndarray]:

    rng = np.random.default_rng(seed)

    idx = rng.integers(0, rated_ratings.size, size=n, dtype=np.int32)
    samples = rated_ratings[idx]  
    event = samples >= 4          
    p_hat = np.mean(event)
    return float(p_hat), event


def simulate_customer_ge_2(counts_per_customer: np.ndarray, n: int = 500_000, seed: int = 42) -> Tuple[float, np.ndarray]:

    rng = np.random.default_rng(seed)

    idx = rng.integers(0, counts_per_customer.size, size=n, dtype=np.int32)
    samples = counts_per_customer[idx]
    event = samples >= 2
    p_hat = np.mean(event)
    return float(p_hat), event


# -----------------------------
# Convergence plot (no Python loop)
# -----------------------------

def convergence_curve(event_bool: np.ndarray) -> np.ndarray:

    cum = np.cumsum(event_bool, dtype=np.int64)
    t = np.arange(1, event_bool.size + 1, dtype=np.int64)
    return cum / t


def plot_convergence(running: np.ndarray, p_theoretical: float, title: str) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(running)               
    plt.axhline(p_theoretical, linestyle="--")
    plt.xlabel("Iteration")
    plt.ylabel("Running estimate")
    plt.title(title)
    plt.grid(True)
    plt.show()


# -----------------------------
# Memory usage reporting
# -----------------------------

def print_memory_report(**arrays) -> None:

    print("\nMemory usage (approx, from NumPy .nbytes):")
    total = 0
    for name, arr in arrays.items():
        if isinstance(arr, np.ndarray):
            mb = arr.nbytes / (1024**2)
            total += arr.nbytes
            print(f"- {name}: {mb:.2f} MB (dtype={arr.dtype}, shape={arr.shape})")
    print(f"- TOTAL shown: {total / (1024**2):.2f} MB")


# -----------------------------
# Main execution + explanations
# -----------------------------

def main() -> None:
    # Load raw data
    ratings_obj, customer_ids = load_ratings_and_customers()

    # --- Theoretical (exact from DB data) ---
    p_exact_rating, rated_ratings = theoretical_p_rating_ge_4(ratings_obj)
    p_exact_customer, unique_customers, counts = theoretical_p_customer_ge_2(customer_ids)

    print("=== Task 5 – Monte Carlo Simulation (NumPy) ===")

    print("\nTheoretical (from DB data, no hardcoding):")
    print(f"1) P(rating ≥ 4 | rating exists) = {format_probability(p_exact_rating)}")
    print("Explanation: This is the share of non-null ratings that are 4 or higher in the database.")

    print(f"2) P(customer rented ≥ 2) = {format_probability(p_exact_customer)}")
    print("Explanation: This is the share of customers (who appear in rentings) that have 2+ rentals in the database.")

    # --- Simulations (>=500,000) ---
    p_sim_rating, event_rating = simulate_rating_ge_4(rated_ratings, n=500_000, seed=42)
    p_sim_customer, event_customer = simulate_customer_ge_2(counts, n=500_000, seed=42)

    print("\nSimulation results (500,000 events each):")
    print(f"1) Simulated P(rating ≥ 4 | rating exists) = {format_probability(p_sim_rating)}")
    print("Explanation: We randomly sampled rated rentals many times and counted how often rating ≥ 4.")

    print(f"2) Simulated P(customer rented ≥ 2) = {format_probability(p_sim_customer)}")
    print("Explanation: We randomly sampled customers many times and counted how often their rental count is ≥ 2.")

    # --- Compare simulation vs theoretical ---
    diff_rating = abs(p_sim_rating - p_exact_rating)
    diff_customer = abs(p_sim_customer - p_exact_customer)

    print("\nComparison (simulation vs theoretical-from-data):")
    print(f"- Rating probability absolute difference: {format_probability(diff_rating)}")
    print(f"- Customer probability absolute difference: {format_probability(diff_customer)}")
    print("Explanation: With many simulations, the estimates should get closer to the theoretical values.")

    # --- Convergence curves + plots ---
    running_rating = convergence_curve(event_rating)
    running_customer = convergence_curve(event_customer)

    plot_convergence(running_rating, p_exact_rating, "Convergence: P(rating ≥ 4 | rating exists)")
    plot_convergence(running_customer, p_exact_customer, "Convergence: P(customer rented ≥ 2)")

    # --- Memory usage considerations ---
    print_memory_report(
        rated_ratings=rated_ratings,
        customer_ids=customer_ids,
        counts_per_customer=counts,
        event_rating=event_rating,
        event_customer=event_customer,
        running_rating=running_rating,
        running_customer=running_customer,
    )

    # --- LLN (simple explanation) ---
    print("\nLaw of Large Numbers (LLN) – simple explanation:")
    print("As we repeat the random simulation many times, the estimated probability becomes more stable and closer to the theoretical value.")
    print("This is visible in the convergence plots: early iterations move a lot, later iterations change less.")

    # --- Bias discussion (simple, important) ---
    print("\nSimulation bias (what could make results misleading):")
    print("- Missing ratings: we ignore NULL ratings, so results describe only rentals that actually have ratings.")
    print("- Customer selection: we select customers uniformly; this answers 'random customer' probability, not 'random rental' probability.")
    print("- Data is the source of truth: if the database is not representative (example: many 5-star ratings), probabilities reflect that.")
    print("- Sampling with replacement: simulations assume each draw is independent, which is standard for Monte Carlo.")

if __name__ == "__main__":
    main()
