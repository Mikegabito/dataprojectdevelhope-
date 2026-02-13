# Person 2 — Conditional Probability (Movie Rental Data)

This section answers “how likely is something, given that something else is already true?”

## What “conditional probability” means

Sometimes “overall probability” is not the full story.
Conditional probability asks:

**What are the chances of A, when we only look at cases where B is true?**

Example:
Instead of asking “How often is a movie Drama?”
we ask “How often is a movie Drama **among movies longer than 100 minutes**?”

This can change the result because we are focusing on a specific group.

---

## 1) P(Genre = Drama | Runtime > 100)

Meaning:
Among movies longer than 100 minutes, how many are Drama?

This tells us if long movies are more likely to be Drama compared to the catalog overall.

---

## 2) P(Rating ≥ 4 | Genre = Comedy)

Meaning:
Among Comedy rentals, how often do we see high ratings (4 or 5)?

This helps compare quality or customer satisfaction for Comedy specifically, instead of mixing all genres.

---

## 3) P(Movie released after 2015 | Movie was rented)

Meaning:
Among the movies that were actually rented, how many are newer than 2015?

This shows whether customers tend to rent newer movies more than the general catalog suggests.

---

## 4) P(Customer is Female | Customer rented at least one movie)

Meaning:
Among customers who have rented at least one movie, how many are Female?

This is different from “how many females exist in the customer table” because it focuses only on active customers.

---

## 5) P(Runtime > 120 | Year of release < 2000)

Meaning:
Among older movies (before 2000), how often are they longer than 120 minutes?

This helps detect patterns in older vs newer movie lengths.

---

## Why we compare conditional vs unconditional

- Unconditional probability describes the full database.
- Conditional probability describes a specific subgroup.

The difference between the two tells us what we learn by focusing on a specific condition.
