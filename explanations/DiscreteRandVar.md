# This document presents the complete solution for the Probability & Statistics homework

using the Movie Rental System database. All probability and statistical measures are computed
manually in accordance with the assignment rules. SQL was used only to extract raw data, while
Python was used for all calculations.

## 1 Discrete Random Variable X: Movie Rating

Let X represent the movie rating of a randomly selected movie from the database. Movie ratings
take discrete numerical values; therefore, X is a discrete random variable. The sample space
consists of all movies that have a non-null rating.
The probability mass function (PMF) of X is defined as:
P(X = x) = (Number of movies with rating x) / (Total number of rated movies)
Using the dataset, the PMF was calculated by counting the frequency of each rating value and
dividing by the total number of rated movies (71).

## 2 Expected Value of X

The expected value of a discrete random variable represents its long-run average. It is calculated
using the formula:

E(X) = Σ x · P(X = x)
Applying this formula to the PMF of movie ratings gives:

E(X) = 2.21

This means that if movies are randomly selected many times, the average rating will converge to
approximately 2.21.

## 3 Variance and Standard Deviation of X

Variance measures how much the values of a random variable spread around the mean. It is
calculated as:

Var(X) = Σ (x − µ)² · P(X = x)
Using µ = E(X) = 2.21, the variance of movie ratings is:

Var(X) = 0.207
The standard deviation is the square root of the variance:

σ = √Var(X) = 0.455

## 4 Discrete Random Variable Y: Number of Movies Rented per Customer

Let Y represent the number of movies rented by a randomly selected customer. This variable is
discrete because customers can only rent whole numbers of movies.
The PMF of Y is defined as:

P(Y = y) = (Number of customers who rented y movies) / (Total number of customers)

## 5 Expected Value and Variance of Y

The expected value of Y is calculated using the same formula for discrete random variables:

E(Y) = Σ y · P(Y = y)
Applying this formula to the rental data gives:
E(Y) = 4.98
This indicates that a customer rents approximately five movies on average.
The variance of Y is computed as:

Var(Y) = Σ (y − µ)² · P(Y = y)
Var(Y) = 9.29

## Interpretation of Expected Value

The expected value does not describe a typical individual movie or customer. Instead, it represents
the long-run average outcome obtained from repeated random selections from the dataset. This
interpretation is fundamental to understanding probability distributions in real-world systems.
