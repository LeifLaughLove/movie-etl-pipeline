
import os
import psycopg2
from dotenv import load_dotenv


# fetch_movie_from_db runs when the user presses the search button, 
# it shows all movies from the database that correspond with the users filters and sort selections

load_dotenv()

def fetch_movies_from_db(
        sort_by,
        min_year,
        max_year,
        genre,
        rating,
        sort_order="ASC"
    ):
    
    """Fetch all movies from the specified table and return as a list of dicts."""
    
    database_url = os.getenv("DATABASE_URL")
    movies = []
    query = f"SELECT * FROM primary_movies WHERE 1=1"
    params = []
    ratings = ['G', 'PG', 'PG-13', 'R']

    if min_year:
        query += " AND release_date >= %s"
        params.append(f"{min_year}-01-01")
    if max_year:
        query += " AND release_date <= %s"
        params.append(f"{max_year}-12-31")


    if genre and genre != "Any":
        query += " AND genres LIKE %s"
        params.append(f"%{genre}%")

        #if rating takes the rating string and allows all ratings at a lower index to be included
    if rating and rating != "Any":
        ratings = ratings[:ratings.index(rating) + 1]
        query += " AND rating IN %s"
        params.append(tuple(ratings))

        #if sort_by orders all movies to be sorted by the users selection and in the users selected order EXAMPLE: title ASC = alphabetical order
    if sort_by:
        query += f" ORDER BY {sort_by} {sort_order}"

    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                movies.append(dict(zip(columns, row)))

    return movies

def fetch_top_rated_movies(limit=10, conn=None):
    with conn.cursor() as cursor:
        cursor.execute