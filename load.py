import json
import os
import psycopg2
from dotenv import load_dotenv
   

def save_to_file(transformed_data, file_name="movies.json"):

    with open(file_name, "w") as file:
        json.dump(transformed_data, file, indent=4)



def save_to_database(transformed_data):


    try: 

        load_dotenv()
        database_url = os.getenv("DATABASE_URL")

        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cursor:


                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movies (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        overview TEXT,
                        popularity FLOAT,
                        vote_average REAL,
                        vote_count INTEGER
                    )
                """)


                for movie in transformed_data:
                    cursor.execute("""
                        INSERT INTO movies (title, overview, popularity, vote_average, vote_count)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (movie["title"], movie["overview"], movie["popularity"], movie["vote_average"], movie["vote_count"]))
                conn.commit()

                print("GREAT SUCCESS")
    
    except Exception as e:

        print(f"Error saving to database: {e}")
        save_to_file(transformed_data) 
