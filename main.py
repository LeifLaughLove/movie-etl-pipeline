import requests
from dotenv import load_dotenv
import os
    
from extract import fetch_movie_data
from transform import transform_movie_data
from load import save_to_file, save_to_database


def main():

    # The load_dotenv() function loads environment variables from a .env file into the Python environment
    load_dotenv()

    #os.getenv("API_KEY") loads the API from the .env file
    API_key = os.getenv("API_KEY")

    # fetch_movie_data(API_Key) takes the API key that was stored in the .env File and passes it to the fetch_movie_data function to 
    # acquire the data from the API, (fetch_movie_data is imported from extract.py)
    raw_data = fetch_movie_data(API_key)

    selected_columns = [
        "title",
        "overview",
        "popularity",
        "vote_count",
        "vote_average"
    ]

    transformed_data = transform_movie_data(raw_data, selected_columns)

    save_to_file(transformed_data)
    save_to_database(transformed_data)


if __name__ == "__main__":
    main()


