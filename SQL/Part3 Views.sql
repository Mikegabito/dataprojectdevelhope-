-- ===========================
--  VIEW: view_movie_summary
-- ===========================
CREATE OR REPLACE VIEW view_movie_summary AS
SELECT 
    m.movie_id,
    m.title,
    g.genre_name,
    d.director_name,
    m.rating AS avg_rating,
    (SELECT COUNT(*) FROM reviews r WHERE r.movie_id = m.movie_id) AS review_count
FROM movies m
LEFT JOIN genres g ON m.genre_id = g.genre_id
LEFT JOIN directors d ON m.director_id = d.director_id;

-- ===========================
--  VIEW: view_actor_summary
-- ===========================
CREATE OR REPLACE VIEW view_actor_summary AS
SELECT 
    a.actor_name,
    COUNT(DISTINCT ac.movie_id) AS number_of_movies,
    AVG(m.rating) AS avg_movie_rating
FROM actors a
LEFT JOIN actsin ac ON a.actor_id = ac.actor_id
LEFT JOIN movies m ON ac.movie_id = m.movie_id
GROUP BY a.actor_id;

-- ===========================
--  VIEW: view_genre_stats
-- ===========================
CREATE OR REPLACE VIEW view_genre_stats AS
SELECT 
    g.genre_name,
    COUNT(m.movie_id) AS total_movies,
    AVG(m.rating) AS avg_genre_rating
FROM genres g
LEFT JOIN movies m ON g.genre_id = m.genre_id
GROUP BY g.genre_id;

-- ======================================
--  VIEW: view_director_performance
-- ======================================
CREATE OR REPLACE VIEW view_director_performance AS
SELECT 
    d.director_name,
    COUNT(m.movie_id) AS number_of_movies,
    AVG(m.rating) AS average_rating
FROM directors d
LEFT JOIN movies m ON d.director_id = m.director_id
GROUP BY d.director_id;
---

