---- 4. Stored Functions
--Create two functions for reusability:
--1. get_actor_avg_rating(actor_id) → returns average rating of all movies that
--actor played in.

--2. get_genre_top_movie(genre_name) → returns the highest-rated movie in that
--genre.

--(Use RETURNS TABLE or RETURNS FLOAT/TEXT depending on your SQL dialect.)


1) CREATE OR REPLACE FUNCTION get_actor_avg_rating(p_actor_id INT)
RETURNS FLOAT AS $$
BEGIN
RETURN
(
SELECT AVG(m.rating)
FROM movies m
JOIN movie_actors ma ON m.movie_id = ma.movie_id
WHERE ma.actor_id = p_actor_id
);
END;
$$ LANGUAGE plpgsql;



2) CREATE OR REPLACE FUNCTION get_genre_top_movie(p_genre TEXT)
RETURNS TABLE (movie_title TEXT, rating FLOAT) AS $$
BEGIN
RETURN QUERY
SELECT m.title, m.rating
FROM movies m
WHERE m.genre = p_genre
ORDER BY m.rating DESC
LIMIT 1;
END;
$$ LANGUAGE plpgsql;
