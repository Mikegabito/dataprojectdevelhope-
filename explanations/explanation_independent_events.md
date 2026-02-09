# Person 3 – Independent vs Dependent Events

This part of the project checks whether two events happen independently, or whether one event seems related to the other.

The key idea is simple:
If two events are independent, then the chance of both happening together should be close to:
P(A and B) ≈ P(A) × P(B)

The program runs two real experiments using the rental database.

Experiment 1 uses rated rentals:
Event A means the rented movie belongs to a specific genre.
Event B means the rental rating is 4 or higher.
The program calculates:

- how often A happens
- how often B happens
- how often A and B happen together
Then it compares P(A and B) with P(A) × P(B).

Experiment 2 uses customers who appear in the rental data:
Event A means the customer has a specific gender.
Event B means the customer rented two or more movies.
The same comparison is made: P(A and B) versus P(A) × P(B).

To avoid guessing values, the program automatically chooses the most common genre and the most common gender found in the data. This ensures the results are based on what actually exists in the database.

The final output shows everything as percentages and includes a short conclusion:

- “approximately independent” if the difference is small
- “likely dependent” if the difference is larger

This makes it easy to see whether the two events look unrelated or connected, based on real data.
