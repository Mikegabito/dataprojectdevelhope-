# Person 6 – Bayes’ Theorem

This part of the project uses Bayes’ Theorem to answer questions like:
“If we already know something is true, how does that change the probability of something else?”

Bayes’ Theorem is useful because it updates a probability when new information is available.

The program uses real data from the database and shows results as percentages.

It runs two examples.

Example 1:
It answers:
“What is the probability that a rental belongs to a certain genre, if the rating is 4 or higher?”

To do that, the program uses rated rentals only and calculates:

- Prior: how common the genre is overall
- Likelihood: how often ratings of 4+ happen inside that genre
- Evidence: how common ratings of 4+ are overall
Then it combines these values to compute the posterior probability using Bayes’ formula.

After that, the program also calculates the same result in a direct way:
It simply looks only at rentals with rating 4+ and checks what percentage of them belong to that genre.
This “direct check” is used to confirm that the Bayes result makes sense.

Example 2:
It answers:
“What is the probability that a rental is from a certain genre, if the customer belongs to a specific gender group?”

The program chooses the most common gender value in the data so the result is based on real usage.
Then it again calculates:

- Prior: how common the genre is overall
- Likelihood: how often the chosen gender appears inside that genre
- Evidence: how common the chosen gender is overall
Then it computes the Bayes posterior and compares it to a direct check.

If the Bayes result and the direct check are close, it means the calculation is consistent and trustworthy.

Overall, this shows how Bayes’ Theorem can turn real database data into updated probabilities that are easy to interpret.
