# Discrete Random Variables & Expected Value

This document provides a detailed, plain-English explanation of the Random Variables
and Linear Algebra task. The goal of the task is to correctly model real-world data using
probability theory and NumPy-based mathematical operations, without using built-in
statistical shortcuts.
A random variable is a numerical value produced by a random process. A random variable
is called discrete when it can only take specific, separate values rather than any value on a
continuous range.
In this assignment, two discrete random variables were defined. The first random variable,
X, represents the rating of a randomly selected movie. The second random variable, Y,
represents the number of movies rented by a randomly selected customer.
Both variables are discrete because movie ratings come from a fixed set of values, and
customers can only rent whole numbers of movies.

## Random Variable X: Movie Ratings

The random variable X represents the rating of a movie chosen at random from the
database. Each movie has exactly one rating, and multiple movies may share the same
rating value.
To compute probabilities, the first step is to count how many times each rating value
appears in the dataset. These counts are then divided by the total number of rated movies.
This process is called normalization and produces the Probability Mass Function (PMF).
The PMF tells us how likely each rating value is. The sum of all probabilities in the PMF is
equal to one, which confirms that the probabilities describe the entire sample space.
The expected value of X represents the long-run average movie rating. It is calculated by
multiplying each rating value by its probability and summing all results.
The expected value does not describe the most common rating or a rating that must exist
in the dataset. Instead, it describes what average value we would observe if we randomly
selected movies many times.

## Variance and Standard Deviation of Movie Ratings

Variance measures how much the movie ratings differ from the expected value. It
quantifies how spread out the ratings are around the average.
To calculate variance, the difference between each rating value and the expected value is
computed. This difference is squared so that negative values do not cancel out positive
ones. Each squared difference is then weighted by its probability.
A small variance indicates that most ratings are close to the average rating. A larger
variance indicates that ratings are more widely spread.
The standard deviation is the square root of the variance. It is easier to interpret because it
is expressed in the same units as the original data.
For movie ratings, the standard deviation tells us how much ratings typically differ from the
average rating.

## Random Variable Y: Movies Rented per Customer

The second random variable, Y, represents the number of movies rented by a randomly
selected customer. Since customers can only rent whole numbers of movies, Y is also a
discrete random variable.
To compute the PMF of Y, the number of movies rented by each customer is first counted.
Customers who rented the same number of movies are grouped together.
The probability of each rental count is calculated by dividing the number of customers in
that group by the total number of customers.
The expected value of Y represents the long-run average number of movies rented per
customer. It does not mean that most customers rent this exact number of movies.
The variance of Y measures how much customer rental behavior varies. A large variance
indicates that some customers rent very few movies, while others rent many.

## Final Interpretation and Conclusion

Expected values represent long-run averages, not predictions for individual cases.
Variance and standard deviation describe how spread out values are around the average.
Using NumPy and linear algebra allows these calculations to closely match their
mathematical definitions while avoiding forbidden statistical shortcuts.
This assignment demonstrates how probability theory can be applied to real-world data to
gain meaningful insights about behavior and variability in a system
