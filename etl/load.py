import json
import logging
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
   
    # save_to_file saves the primary data to a JSON file

def save_to_file(primary_data, primary_movies_file="primary_movies.json"):

    with open(primary_movies_file, "w") as file:
        json.dump(primary_data, file, indent=4)


    # save_to_database function takes the primary data and saves it to a database
def save_to_database(primary_data):


    try: 

        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        print(f"Loaded DB URL: {database_url}")

        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cursor:

#-----------------             
   
                # CREATE TABLE IF NOT EXISTS allows new movie data to be appended to exisitng data
                # an incramenting id is given to each movie as a PRIMARY KEY
                # tmdb_id INTEGER UNIWUE ensures no duplicate movies are inserted into the database

                logging.info("Creating tables in database...")

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS primary_movies (
                        id SERIAL PRIMARY KEY,
                        tmdb_id INTEGER UNIQUE,
                        title TEXT,
                        overview TEXT,
                        popularity FLOAT,
                        vote_average REAL,
                        vote_count INTEGER,
                        release_date DATE,
                        rating TEXT,
                        genres TEXT
                    );
                """)

#-----------------

                logging.info("Inserting data into database tables...")

                # FOR LOOP iterates over each movie, formats release date 
                # ensures there is no duplicate ON CONFLICT with tmdb_id

                for movie in primary_data:
                    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").date() if movie.get("release_date") else None
                    cursor.execute("""
                        INSERT INTO primary_movies (tmdb_id, title, overview, popularity, vote_average, vote_count, release_date, rating, genres)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (tmdb_id) DO NOTHING;
                    """, (
                        movie["id"],
                        movie["title"], 
                        movie["overview"], 
                        movie["popularity"], 
                        movie["vote_average"], 
                        movie["vote_count"], 
                        release_date, 
                        movie['rating'],
                        movie["genres"]
                    ))

                # commit the changes to the database
                conn.commit()

                logging.info("Data saved to database successfully.")

    
    except Exception:
        logging.error("Error saving to database:", exc_info=True) 
