
-- Query 1: Top 5 movies by average rating (using view_movie_summary)
SELECT
  title,
  genre,
  avg_rating,
  review_count
FROM view_movie_summary
ORDER BY avg_rating DESC NULLS LAST, review_count DESC
LIMIT 5;

-- Query 2: Number of movies per actor
SELECT
  a.actor_id,
  a.name AS actor_name,
  COUNT(DISTINCT ai.movie_id) AS movie_count
FROM actors a
LEFT JOIN actsin ai
  ON ai.actor_id = a.actor_id
GROUP BY a.actor_id, a.name
ORDER BY movie_count DESC, actor_name;

-- Query 3: Actors whose average movie rating is greater than 7
SELECT
  a.actor_id,
  a.name AS actor_name,
  get_actor_avg_rating(a.actor_id) AS avg_rating
FROM actors a
WHERE get_actor_avg_rating(a.actor_id) > 7
ORDER BY avg_rating DESC;

-- Query 4: Actors who appeared in more than 3 movies
SELECT
  a.actor_id,
  a.name AS actor_name,
  COUNT(DISTINCT ai.movie_id) AS movie_count
FROM actors a
JOIN actsin ai
  ON ai.actor_id = a.actor_id
GROUP BY a.actor_id, a.name
HAVING COUNT(DISTINCT ai.movie_id) > 3
ORDER BY movie_count DESC, actor_name;

-- Query 5: Movies that have no reviews (no rows in rentings)
SELECT
  m.movie_id,
  m.title,
  m.genre,
  m.year_of_release
FROM movies m
LEFT JOIN rentings r
  ON r.movie_id = m.movie_id
WHERE r.renting_id IS NULL
ORDER BY m.movie_id;

-- Query 6: Youngest actor in each genre
WITH actor_genre AS (
  SELECT DISTINCT
    m.genre,
    a.actor_id,
    a.name,
    a.year_of_birth
  FROM actors a
  JOIN actsin ai
    ON ai.actor_id = a.actor_id
  JOIN movies m
    ON m.movie_id = ai.movie_id
),
ranked AS (
  SELECT
    genre,
    actor_id,
    name,
    year_of_birth,
    ROW_NUMBER() OVER (PARTITION BY genre ORDER BY year_of_birth DESC) AS rn
  FROM actor_genre
)
SELECT
  genre,
  actor_id,
  name AS actor_name,
  year_of_birth
FROM ranked
WHERE rn = 1
ORDER BY genre;

-- Query 7: Genres whose average rating is higher than the overall average rating
WITH overall AS (
  SELECT AVG(r.rating) AS overall_avg_rating
  FROM rentings r
  WHERE r.rating IS NOT NULL
)
SELECT
  m.genre,
  AVG(r.rating) AS avg_genre_rating,
  (SELECT overall_avg_rating FROM overall) AS overall_avg_rating
FROM movies m
JOIN rentings r
  ON r.movie_id = m.movie_id
WHERE r.rating IS NOT NULL
GROUP BY m.genre
HAVING AVG(r.rating) > (SELECT overall_avg_rating FROM overall)
ORDER BY avg_genre_rating DESC;

-- Query 8: Actors who never appeared in a movie rated below 5
SELECT
  a.actor_id,
  a.name AS actor_name,
  MIN(r.rating) AS min_rating,
  AVG(r.rating) AS avg_rating
FROM actors a
JOIN actsin ai
  ON ai.actor_id = a.actor_id
JOIN rentings r
  ON r.movie_id = ai.movie_id
WHERE r.rating IS NOT NULL
GROUP BY a.actor_id, a.name
HAVING MIN(r.rating) >= 5
ORDER BY avg_rating DESC, actor_name;

-- Query 9: Total movies, number of reviews, and average rating per release year
SELECT
  m.year_of_release,
  COUNT(DISTINCT m.movie_id) AS total_movies,
  COUNT(r.rating) AS total_reviews,
  AVG(r.rating) AS avg_rating
FROM movies m
LEFT JOIN rentings r
  ON r.movie_id = m.movie_id
GROUP BY m.year_of_release
ORDER BY m.year_of_release;

-- Query 10: Most active reviewer (customer with the highest number of ratings)
SELECT
  c.customer_id,
  c.name AS customer_name,
  COUNT(r.rating) AS review_count
FROM customers c
JOIN rentings r
  ON r.customer_id = c.customer_id
WHERE r.rating IS NOT NULL
GROUP BY c.customer_id, c.name
ORDER BY review_count DESC
LIMIT 1;

-- Query 11: Average runtime and total movies per genre
SELECT
  genre,
  COUNT(*) AS total_movies,
  AVG(runtime) AS avg_runtime
FROM movies
GROUP BY genre
ORDER BY avg_runtime DESC;

-- Query 12: Average number of movies rented per active customer
WITH customer_stats AS (
  SELECT
    c.customer_id,
    c.name AS customer_name,
    COUNT(r.renting_id) AS total_rentings
  FROM customers c
  JOIN rentings r
    ON r.customer_id = c.customer_id
  GROUP BY c.customer_id, c.name
)
SELECT
  AVG(total_rentings)::NUMERIC(10,2) AS avg_movies_per_active_customer
FROM customer_stats;
