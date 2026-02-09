# Task 3 – Independence Testing (NumPy)

This task checks whether two events appear independent or dependent using real data.

The basic rule is:
If two events are independent, then the probability of both happening together should be close to:
P(A and B) ≈ P(A) × P(B)

The program loads rental data that includes:

- movie genre
- movie runtime
- rental rating
- customer gender

Then it creates events using NumPy Boolean masks.
A Boolean mask is a True/False list that identifies which rows match a condition.

For each event pair, the program calculates:

- P(A): how often event A happens
- P(B): how often event B happens
- P(A and B): how often both happen together
- P(A) × P(B): what we would expect if they were independent

Because decimal calculations can have small rounding differences, the program uses a tolerance threshold.
If the difference between P(A and B) and P(A) × P(B) is small enough, it labels the pair as “approximately independent.”

Important requirement:
One pair is intentionally designed to be clearly dependent.
In Pair 3:
A = rating is 4 or higher
B = rating is 3 or higher

This is dependent because every rating that is 4 or higher is automatically also 3 or higher.
So the chance of A changes when we know B is true.

All results are displayed as percentages in a table so the comparison is easy to understand.
