import json
import logging
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
   
    # save_to_file saves the primary and secondary datas to two seperate json files, the data is brought in as arguments, and the files are named in the function

def save_to_file(primary_data, secondary_data, primary_movies_file="primary_movies.json", secondary_movies_file="secondary_movies.json"):

    with open(primary_movies_file, "w") as file:
        json.dump(primary_data, file, indent=4)
    
    with open(secondary_movies_file, "w") as file:
        json.dump(secondary_data, file, indent=4)


    # save_to_database function takes the primary and secondary data as arguments and saves them to a PostgreSQL database
def save_to_database(primary_data, secondary_data):


    try: 

        load_dotenv()
        database_url = os.getenv("DATABASE_URL")

        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cursor:

#-----------------                
                # DROP TABLE IF EXISTS for primary and secondary movies ensures two brand new tables are created each time the function is run
                # This prevents any duplicate data from being inserted into the database
                logging.info("Creating tables in database...")

                cursor.execute("DROP TABLE IF EXISTS primary_movies, secondary_movies")
                cursor.execute("""
                    CREATE TABLE primary_movies (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        overview TEXT,
                        popularity FLOAT,
                        vote_average REAL,
                        vote_count INTEGER,
                        release_date DATE,
                        adult BOOLEAN DEFAULT FALSE
                    );
                """)

                cursor.execute("""
                    CREATE TABLE secondary_movies (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        overview TEXT,
                        popularity FLOAT,
                        vote_average REAL,
                        vote_count INTEGER,
                        release_date DATE,
                        adult BOOLEAN DEFAULT FALSE
                    );
                """)
#-----------------

                logging.info("Inserting data into database tables...")

                # for loop iterates through each movie in the primary data and inserts it, along with the selected columns, into the database
                for movie in primary_data:
                    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").date() if movie.get("release_date") else None
                    cursor.execute("""
                        INSERT INTO primary_movies (title, overview, popularity, vote_average, vote_count, release_date, adult)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (movie["title"], 
                        movie["overview"], 
                        movie["popularity"], 
                        movie["vote_average"], 
                        movie["vote_count"], 
                        release_date, 
                        movie["adult"]))


                # for loop iterates through each movie in the secondary data and inserts it, along with the selected columns, into the database
                for movie in secondary_data:
                    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").date() if movie.get("release_date") else None
                    cursor.execute("""
                        INSERT INTO secondary_movies (title, overview, popularity, vote_average, vote_count, release_date, adult)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (movie["title"], 
                        movie["overview"], 
                        movie["popularity"], 
                        movie["vote_average"], 
                        movie["vote_count"], 
                        release_date, 
                        movie["adult"]))

                # commit the changes to the database
                conn.commit()

                logging.info("Data saved to database successfully.")

    
    except Exception:
        logging.error("Error saving to database:", exc_info=True) 
