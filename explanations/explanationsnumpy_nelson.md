# Task 5 – Monte Carlo Simulation (NumPy Version)

Probability & Statistics with Python – Movie Rental System

What Is the Goal of This Task?
The goal of this task is to estimate probabilities using random experiments, instead of formulas.
This method is called Monte Carlo simulation, and it is based on repeating a random process many times and observing what happens.
Instead of guessing or assuming probabilities, we let the data itself tell us what is likely to happen.

## Where Does the Data Come From?

The data comes from the movie rental database, specifically from the table that stores rental information.
For this task, we only use:
Movie ratings (some rentals have ratings, some do not)
Customer IDs (to know how many movies each customer rented)
The database is accessed live.
SQL is used only to read the data, and all calculations are done using Python with NumPy.

## First Question: How Likely Is a Movie Rating of 4 or Higher?

What Are We Trying to Answer?
We want to answer this simple question:
“If we randomly choose a movie rental that has a rating, how likely is it that the rating is 4 or higher?”
We only look at rentals that actually have a rating, because it would not make sense to include missing ratings.

Exact Answer from the Data
First, we calculate the answer directly from the database:
We count how many ratings are 4 or higher
We divide by the total number of rentals that have a rating
This gives us the exact value based on the data, and we use it as a reference.

## Random Simulation (Monte Carlo)

Then we estimate the same probability using simulation:
All valid ratings are stored in a list.
The computer randomly picks 500,000 ratings from this list.
Each time, it checks if the rating is 4 or higher.
The probability is estimated by checking how often this happens.
No values are guessed or manually inserted.
Everything comes from repeated random selection.

## Second Question: How Likely Is a Customer to Rent Two or More Movies?

What Are We Trying to Answer?
Now we ask a different question:
“If we randomly choose a customer who appears in the rental data, how likely is it that they rented at least two movies?”

This helps us understand customer behavior.
Exact Answer from the Data
To find the exact answer:
We count how many movies each customer rented
We count how many customers rented two or more movies
We divide by the total number of customers
This gives the real probability based on all available data.

## Random Simulation

To estimate this probability using simulation:
The number of rentals per customer is stored.
The computer randomly selects 500,000 customers.
Each time, it checks whether the customer rented two or more movies.
The probability is estimated by how often this condition is true.
Again, no assumptions are made — everything comes from the data.

## Why Do the Results Become More Stable Over Time?

At the beginning of the simulation, results change a lot.
As more and more random selections are made, the result changes less and less.
This happens because of a principle called the Law of Large Numbers, which simply means:
“When you repeat a random experiment many times, the average result becomes more reliable.”
This behavior is shown visually using a convergence plot, where the estimated probability slowly settles around the exact value.

## Memory Usage (Why It Matters)

This task uses 500,000 random events, which means the computer needs to store a lot of data.
To keep memory usage reasonable:
Efficient data storage is used
Only necessary information is kept
Memory usage is measured and reported
This shows that large simulations can be done without wasting resources.
Possible Limitations and Bias
Even though the simulation is correct, it is important to understand its limits:
Missing ratings: Rentals without ratings are ignored, so results only apply to rated rentals.
Customer selection: Customers are chosen evenly, which answers “random customer” questions, not “random rental” questions.
Data bias: If most ratings are high, the probability of high ratings will naturally be high.
Random repetition: The same customer or rating can be selected more than once, which is normal in this type of simulation.
These points do not invalidate the results, but they help explain how to interpret them correctly.

## Final Conclusion

This task shows how probabilities can be estimated using random simulation and real data, without relying on formulas or assumptions.
By repeating random selections many times:
The estimated probabilities become more reliable
The results match closely with the exact values from the database
The Law of Large Numbers is clearly demonstrated
Overall, Monte Carlo simulation provides an intuitive and practical way to understand probability, even without advanced mathematical knowledge.-
