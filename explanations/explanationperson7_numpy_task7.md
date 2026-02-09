# Task 7 – Statistical Experiment & Reporting (NumPy)

This file designs a simple experiment and reports results like a small research study.

The question studied is:
“What is the probability that a rental rating is 4 or higher?”

The program loads all available ratings into a NumPy array.
Then it runs the same experiment at multiple sample sizes (for example: 100, 1,000, 10,000, and more).

For each sample size, it randomly samples ratings and estimates the probability of rating 4 or higher.
As sample size increases, the estimate becomes more stable and closer to the exact value calculated from all data.

A plot is created to visualize convergence.
The x-axis uses a log scale so we can clearly see improvement across small and large sample sizes.

Noise vs signal:
Small samples are noisy, so estimates can move around more.
Large samples reduce noise and reveal the real pattern in the data.

Limitations:
This experiment only uses the ratings that exist in the database.
If ratings are missing for many rentals, the conclusion is about “rated rentals,” not all rentals.

## Conclusion

The estimates become more stable as the sample size grows, and they move closer to the exact value from the full dataset. This supports the idea that larger samples reduce random noise and reveal the real probability pattern in the data.
