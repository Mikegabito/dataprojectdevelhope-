# Person 1 — Basic Probability (Movie Rental Data)

This section answers simple questions like “How likely is it?” using the movie rental data.

Probability is basically:
**(how many times something happens) ÷ (how many total cases we are looking at)**

The results are printed as percentages to make them easy to read.

---

## 1) Movie length categories (runtime)

We group movies into 5 length groups:

- under 80 minutes
- 80–99 minutes
- 100–119 minutes
- 120–149 minutes
- 150+ minutes

Then we calculate how often each group appears.

This helps describe the catalog: mostly short movies, mostly medium, or lots of long movies.

---

## 2) Newer vs older movies

We calculate the chance that a movie is newer than:

- 2000
- 2010
- 2020

This gives a quick idea of how modern the movies are in the database.

---

## 3) Ratings behavior

We calculate:

- how often rentals have a rating at all
- among rated rentals, how common each rating value (1 to 5) is

This shows how often customers leave feedback and what the feedback tends to look like.

---

## 4) Genre distribution

We calculate the probability of each genre based on the rental records.

This shows what types of movies are being rented most often in the dataset.

---

## 5) Customer distribution (country + gender)

We calculate the probability of each country and gender based on rental rows.

This provides a simple view of who is renting movies in the stored data.
It only describes what is recorded — it does not explain why.
