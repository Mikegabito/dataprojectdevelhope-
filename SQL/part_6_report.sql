Report 1: Top 3 Genres by Total Reviews

SELECT g.genre_name, SUM(m.review_count) AS total_reviews
FROM genres g
JOIN movies m ON g.genre_id = m.genre_id
GROUP BY g.genre_name
ORDER BY total_reviews DESC
LIMIT 3;

Report 2: Top 5 Actors by Total Appearances

SELECT a.actor_name, COUNT(actsin.movie_id) AS total_appearances
FROM actors a
JOIN actsin ON a.actor_id = actsin.actor_id
GROUP BY a.actor_name
ORDER BY total_appearances DESC
LIMIT 5;

Report 3: Director Performance by Average Movie Rating (min 2 movies)

SELECT d.director_name, COUNT(m.movie_id) AS total_movies,
       ROUND(AVG(m.avg_rating), 2) AS avg_director_rating
FROM directors d
JOIN movies m ON d.director_id = m.director_id
GROUP BY d.director_name
HAVING COUNT(m.movie_id) >= 2
ORDER BY avg_director_rating DESC;

Report 4: Movies with Reviews After 2020

SELECT DISTINCT m.title, m.release_year, m.avg_rating,
       COUNT(r.review_id) AS num_reviews_after_2020
FROM movies m
JOIN reviews r ON m.movie_id = r.movie_id
WHERE EXTRACT(YEAR FROM r.created_at) > 2020
GROUP BY m.movie_id, m.title, m.release_year, m.avg_rating
ORDER BY num_reviews_after_2020 DESC;

Report 5: Genres by Average Duration

SELECT g.genre_name, ROUND(AVG(m.duration), 2) AS avg_duration_minutes
FROM genres g
JOIN movies m ON g.genre_id = m.genre_id
GROUP BY g.genre_name
ORDER BY avg_duration_minutes DESC;
