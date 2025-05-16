import requests
import logging


    # fetch_movie_data function takes the API as an argument and uses the requests library to make a GET request to the API
    # It then converts response to a json file and stores it in a variable called data


def fetch_movie_data(API_key, genre_list):

    all_results = []
    
    try:
            # for loop iterates the the firswt 20 pages of the API
            # The params dictionary contains the parameters for the API request
            # The API key is passed as a parameter, along with the date range and genre (horror)
        for page in range(1, 21):
            params = {
                "api_key": API_key,
                "primary_release_date.gte": "2000-01-01",
                "primary_release_date.lte": "2015-12-31",
                "page": page,
                "with_genres": genre_list
            }
            response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={API_key}", params=params)

            # checks if the response code is NOT 200, 200 means the request was successful
            # if request was not successful it raises an exception with the error code

            if response.status_code != 200:
                raise Exception(f"Error fetching data from API: {response.status_code}")
            
            # if the request was successful it converts the response to a json file and stores it in a variable called data
            # The data is then appended to the all_results list
            data = response.json()
            all_results.extend(data.get("results", []))
            
        logging.info(f"Fetched {len(all_results)} movies from the API")
            
    
    except Exception:
        logging.error("Error fetching data from API:", exc_info=True)
    
    

    return all_results