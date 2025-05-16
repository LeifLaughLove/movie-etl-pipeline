import requests
from dotenv import load_dotenv
import os
import logging    
from extract import fetch_movie_data
from transform import transform_movie_data
from load import save_to_file, save_to_database
import psycopg2


                        # Initialize logging configuration 
logging.basicConfig(
    level=logging.INFO,                                 # sets the minimum logging level to INFO and includes all levels above it (WARNING< ERROR< CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s", #sets the format for log messages (timestamp, log level, and message)
    handlers=[                                          # handlers[] defines where the log messages will be sent 
        logging.FileHandler("etl_pipeline.log"),        #saves log messages to a file named etl_pipeline.log
        logging.StreamHandler()                         #also sends log messages to the console
    ]
)
                        # :START OF THE ETL PIPELINE:
                        # The ETL pipeline is a process that takes data from an API, transforms it, and loads it into a PostgreSQL database, along with a JSON file
                        # First the API key is loaded from a .env file, then in extract.py the API (TMDB) is called and the data is fetched, the fetch function filters the data by genre (HORROR, genre ID 27), release date (2000-2015)
                        # The data is then transformed in the transform.py file, it is filtered into primary data (movies with a vote_copunt between 75 and 400 and a vote_average greater than 0) and secondary data (movies with a vote_count less than 75 or greater than 400 or a vote_average of 0)
                        # the load.py file takes the primary and secondary data and puts it into the two PostgreSQL tables and also saves the data to two JSON files
                        # The main function is the entry point of the ETL pipeline, it orchestrates the entire process by calling the other functions in the correct order
def main():
    logging.info("ETL pipeline started")

    # The load_dotenv() function loads environment variables from a .env file into the Python environment
    load_dotenv()

    #os.getenv("API_KEY") loads the API from the .env file
    API_key = os.getenv("API_KEY")

    # genre list is a list of genre ID's to filter the movies by
    # The genre ID for horror movies is 27 
    genre_list = [27]

    # fetch_movie_data(API_Key) takes the API key that was stored in the .env File and passes it to the fetch_movie_data function to 
    # acquire the data from the API, (fetch_movie_data is imported from extract.py)
    raw_data = fetch_movie_data(API_key, genre_list)


    # selected_columns is a list of the columns to be extracted from the API data
    selected_columns = [
        "title",
        "overview",
        "popularity",
        "vote_count",
        "vote_average",
        "release_date",
        "adult"
    ]

    # transform_movie_data function takes raw_data and selected_columns as arguments
    # It retuurns two lists: primrary_data and secondary_data

    primary_data, secondary_data = transform_movie_data(raw_data, selected_columns)

    #save_to_file function takes priamry and secondary data as arguments and saves them to two seperate JSON files
    #save_to_database functiont takes the primary and secondaery data as arguments and saves them to a PostgreSQL database
    save_to_file(primary_data, secondary_data)
    save_to_database(primary_data, secondary_data)



if __name__ == "__main__":
    main()


