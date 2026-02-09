---Create 3–4 triggers that add automation:
--1. Update average rating trigger:
--When a new review is added → update the movie’s rating.
--2. Review validation trigger:
--Prevent insertion if stars are not between 1–5.
--3. Delete protection trigger:
--Prevent deleting a movie that still has linked reviews or actsin rows.
--4. Logging trigger (optional):
--Create a log_activity table to record whenever a movie or review is
---inserted/deleted.

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(movie_id),
    stars INT,
    comment TEXT
);
CREATE OR REPLACE FUNCTION update_avg_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE rentings
    SET avg_rating = (
        SELECT COALESCE(AVG(stars), 0)
        FROM reviews
        WHERE movie_id = NEW.movie_id
    )
    WHERE movie_id = NEW.movie_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_avg_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE rentings
    SET avg_rating = (
        SELECT COALESCE(AVG(stars), 0)
        FROM reviews
        WHERE movie_id = NEW.movie_id
    )
    WHERE movie_id = NEW.movie_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_avg_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE rentings
    SET avg_rating = (
        SELECT COALESCE(AVG(stars), 0)
        FROM reviews
        WHERE movie_id = NEW.movie_id
    )
    WHERE movie_id = NEW.movie_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_avg_rating
AFTER INSERT ON reviews
FOR EACH ROW
EXECUTE FUNCTION update_avg_rating();

CREATE FUNCTION validate_review()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stars < 1 OR NEW.stars > 5 THEN
        RAISE EXCEPTION 'Ratings must be between 1 and 5.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_review
BEFORE INSERT ON reviews
FOR EACH ROW
EXECUTE FUNCTION validate_review();

CREATE FUNCTION prevent_movie_delete()
RETURNS TRIGGER AS $$
DECLARE
    review_count INT;
    actsin_count INT;
BEGIN
    SELECT COUNT(*) INTO review_count FROM reviews WHERE movie_id = OLD.movie_id;
    SELECT COUNT(*) INTO actsin_count FROM acts_in WHERE movie_id = OLD.movie_id;

    IF review_count + actsin_count > 0 THEN
        RAISE EXCEPTION 'Cannot delete movie: linked reviews or acts_in records exist.';
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_movie_delete
BEFORE DELETE ON movies
FOR EACH ROW
EXECUTE FUNCTION prevent_movie_delete();

CREATE TABLE log_activity (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    action_type VARCHAR(20),
    record_id INT,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE FUNCTION log_movie_activity()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_activity (table_name, action_type, record_id)
    VALUES ('movies', 'INSERT', NEW.movie_id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_movie_activity
AFTER INSERT ON movies
FOR EACH ROW
EXECUTE FUNCTION log_movie_activity();

CREATE FUNCTION log_review_activity()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_activity (table_name, action_type, record_id)
    VALUES ('reviews', 'DELETE', OLD.review_id);

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_review_activity
AFTER DELETE ON reviews
FOR EACH ROW
EXECUTE FUNCTION log_review_activity();

