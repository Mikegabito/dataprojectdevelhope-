# Task 6 – Bayes’ Theorem (NumPy)

This file uses Bayes’ Theorem to update probabilities when we learn new information.

Bayes’ Theorem combines three pieces:

- Prior: how common something is overall
- Likelihood: how common the evidence is inside the group we care about
- Evidence: how common the evidence is overall

The program computes the posterior probability using the Bayes formula:
Posterior = (Likelihood × Prior) ÷ Evidence

Example 1 answers:
“What is the probability a rental is from a certain genre, if the rating is 4 or higher?”

Example 2 answers:
“What is the probability a rental is from a certain genre, if the customer has a certain gender?”

All calculations are done using NumPy arrays and Boolean masks.
After computing the Bayes result, the program also verifies it using a direct conditional calculation.
If both values are close, it confirms the result is consistent.

Normalization is important because without dividing by Evidence, the result can become impossible (larger than 100%).
