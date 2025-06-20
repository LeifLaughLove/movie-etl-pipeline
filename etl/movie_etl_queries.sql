-- Table: primary_movies
-- Columns: id, tmdb_id, title, overview, popularity, vote_average, vote_count, release_date, rating, genres

-- 1. Top 10 highest rated movies
SELECT title, vote_average
FROM primary_movies
ORDER BY vote_average DESC
LIMIT 10;

-- 2. Count of movies by genre
SELECT genres, COUNT(*) 
FROM primary_movies
GROUP BY genres;

-- 3. Movies released after 2010 with 'PG-13' or lower rating
SELECT title, release_date, rating
FROM primary_movies
WHERE release_date > '2010-01-01'
  AND rating IN ('G', 'PG', 'PG-13');