# Sampling & Monte Carlo Simulation

Probability & Statistics with Python – Movie Rental System

Introduction

The purpose of this part of the project is to use random simulation to estimate probabilities related to a movie rental system. Instead of calculating probabilities only by hand, this approach uses random sampling (Monte Carlo simulation) to approximate results based on real data.
All simulations are done using Python’s random module. No probabilities are hardcoded. The results depend entirely on what is observed during the simulations.

## Data Source

The data comes from the rentings table in the database. Only two columns are used:
rating: the rating given to a rented movie (some rentals do not have a rating)
customer_id: identifies which customer made the rental
The database is accessed live using Supabase. SQL is used only to extract the raw data, while all probability calculations and simulations are performed in Python.

## Simulation of Movie Ratings (Rating ≥ 4)

Goal

The first goal is to estimate the probability that a randomly selected movie rental has a rating of 4 or higher.
Because not all rentals have a rating, only rentals with a rating are considered. In simple terms, the question is:
“If we randomly choose a rental that has a rating, what is the chance that the rating is at least 4?”

## How the Simulation Works

A rental is randomly selected from the database.
If the rental does not have a rating, it is ignored.
If the rental has a rating, we check whether it is 4 or higher.
This process is repeated 10,000 times.
The probability is estimated by counting how often the condition is true.
This method does not assume any probability in advance.
The estimate comes purely from random sampling.
Comparison with the Exact Probability

To verify the simulation, an exact probability is also calculated directly from the database by counting:

- how many rentals with a rating have a value of 4 or higher

- how many rentals have a rating in total

The simulated probability is then compared with this exact value. The two results are very close, which shows that the simulation provides a good approximation.

## Simulation of Customer Behavior (Renting ≥ 2 Movies)

Goal

The second goal is to estimate the probability that a random customer has rented two or more movies.
In simple words:

“If we randomly choose a customer who appears in the rental data, what is the chance that they rented at least two movies?”
How the Simulation Works

The total number of rentals for each customer is counted.
In each simulation step, a random customer is selected.
The program checks whether that customer rented two or more movies.
This process is repeated 10,000 times.
The probability is estimated by how often the condition is true.
Again, the result is based only on observed data and random sampling.

Increasing the Simulation Size and Convergence

To better understand how reliable the simulation is, the same simulation for movie ratings is repeated using different numbers of trials, such as:

- 100
- 500
- 1,000
- 5,000
- 10,000
- 50,000

As the number of simulations increases, the estimated probability becomes more stable and closer to the exact value calculated from the database.

## Law of Large Numbers (Simple Explanation)

The Law of Large Numbers explains why this happens. It states that:

“When a random experiment is repeated many times, the average result tends to get closer to the true value.”
In this project:
Small numbers of simulations produce results that vary more.
Larger numbers of simulations produce results that change less.
The estimated probability becomes more reliable as the simulation size increases.
This behavior is clearly visible in both the numerical results and the convergence output.

## Visualization

To make the results easier to understand, a convergence plot is created using Matplotlib.

The plot shows:

how the estimated probability changes as the number of simulations increases
a horizontal line representing the exact probability
This visual representation clearly shows the simulated values approaching the exact value, which supports the explanation of the Law of Large Numbers.

Cumulative probability Plot

What is the probability that a rating is greater than or equal to a given value?
A cumulative probability plot was used to directly show the probability that a rating is greater than or equal to a given value, which makes the interpretation of P(rating ≥ 4) more intuitive.

## final Conclusion

This project demonstrates how Monte Carlo simulation can be used to estimate probabilities using real-world data. By randomly sampling movie rentals and customer behavior, probabilities can be approximated without hardcoding any values.
The close match between simulated and exact probabilities confirms the accuracy of the simulation, while the convergence study explains why increasing the number of simulations leads to more stable and reliable results. Overall, this approach provides a simple and intuitive way to understand probability through programming and data.-
