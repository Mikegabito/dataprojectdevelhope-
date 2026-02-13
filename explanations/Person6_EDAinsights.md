# Person 6 — Exploratory Data Analysis (EDA) Insights

In this section, we explore patterns and unusual values in the data.

EDA helps answer:

- Is the data balanced?
- Are there extreme values?
- Which categories dominate?

---

## 1) Outlier Detection

We use the IQR method to detect extreme values.

An outlier is a value that is much higher or lower than the rest of the data.

We check:

- Movie runtime
- Renting price
- Average rating

Outliers may indicate:

- Very long or very short movies
- Unusually expensive rentals
- Ratings that are extreme compared to others

---

## 2) Most Frequent Categories

We use value_counts() to see:

- Top 5 most common genres
- Top 5 countries
- Top 5 most rented movies

This shows concentration patterns.

If a few categories dominate, the dataset is not evenly distributed.

---

## 3) Insights

Insight 1  
Some numerical columns contain extreme values, which may influence averages.

Insight 2  
A small number of genres represent most rentals, indicating strong customer preference patterns.

Insight 3  
A few movies dominate rental activity, meaning demand is concentrated rather than evenly spread.

---

## Why EDA Is Important

EDA is the step before advanced modeling.

It helps:

- Detect data quality issues
- Understand customer behavior
- Identify concentration trends
- Spot anomalies early
