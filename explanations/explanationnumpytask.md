# Task 1 – Vectorized Probability Distributions (NumPy)

This task uses real rental and movie data to calculate probabilities about movie runtimes.

The program connects to the database and loads three columns:

- runtime (movie length)
- genre (movie category)
- rating (user rating, which can be missing)

Because databases can contain missing values, the program converts missing values into NaN (a standard “missing number” marker).
This makes it possible to filter valid numbers safely.

The main goal is to build a probability distribution for runtime categories:

- shorter than 80 minutes
- 80–99 minutes
- 100–119 minutes
- 120–149 minutes
- 150 minutes or longer

Instead of checking values one by one, the program uses NumPy Boolean masks.
A Boolean mask is simply a True/False list that marks which rows belong to a category.

For each category, the probability is calculated as:
(number of movies in the category) ÷ (number of movies with a valid runtime)

All results are printed as percentages to make them easy to interpret.

At the end, the program performs a manual verification for one category (100–119 minutes) to confirm that the vectorized result matches the direct counting method.
This builds confidence that the distribution is correct.
.
