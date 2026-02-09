-- ================================================
-- Part 1 – Relationships & Constraints
-- Implemented for Team 1 – Movie Renting Database
-- ================================================

-- ------------------------------------------------
-- 1. CHECK CONSTRAINTS
-- ------------------------------------------------

-- Ensures renting ratings are valid values between 0 and 10.
ALTER TABLE rentings
    ADD CONSTRAINT chk_rentings_rating_between_0_10
    CHECK (rating BETWEEN 0 AND 10);

-- Ensures every actor has a valid name (not NULL and not empty).
ALTER TABLE actors
    ALTER COLUMN name SET NOT NULL;

ALTER TABLE actors
    ADD CONSTRAINT chk_actors_name_not_empty
    CHECK (length(trim(name)) > 0);

-- Ensures that movie release years are realistic.
ALTER TABLE movies
    ADD CONSTRAINT chk_movies_year_of_release_min_1900
    CHECK (year_of_release >= 1900);

-- Prevents duplicate movies with same title & release year.
ALTER TABLE movies
    ADD CONSTRAINT uq_movies_title_year_of_release
    UNIQUE (title, year_of_release);

-- ------------------------------------------------
-- 2. FOREIGN KEYS (ON DELETE CASCADE)
-- ------------------------------------------------

-- Links actsin.movie_id → movies.movie_id
ALTER TABLE actsin
    ADD CONSTRAINT fk_actsin_movie
    FOREIGN KEY (movie_id)
    REFERENCES movies(movie_id)
    ON DELETE CASCADE;

-- Links actsin.actor_id → actors.actor_id
ALTER TABLE actsin
    ADD CONSTRAINT fk_actsin_actor
    FOREIGN KEY (actor_id)
    REFERENCES actors(actor_id)
    ON DELETE CASCADE;

-- Links rentings.customer_id → customers.customer_id
ALTER TABLE rentings
    ADD CONSTRAINT fk_rentings_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
    ON DELETE CASCADE;

-- Links rentings.movie_id → movies.movie_id
ALTER TABLE rentings
    ADD CONSTRAINT fk_rentings_movie
    FOREIGN KEY (movie_id)
    REFERENCES movies(movie_id)
    ON DELETE CASCADE;

-- ------------------------------------------------
-- 3. GENRE VALIDATION (schema adaptation)
-- ------------------------------------------------

-- Ensures that each movie has a valid genre.
-- Your schema does not include genre_id, so we enforce NOT NULL on the genre column.
ALTER TABLE movies
    ALTER COLUMN genre SET NOT NULL;

-- ================================================
-- END OF PART 1
-- ================================================
