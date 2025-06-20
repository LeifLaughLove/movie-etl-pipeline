import requests
import logging


    # fetch_movie_data function takes the API as an argument and uses the requests library to make a GET request to the API
    # It then converts response to a json file and stores it in a variable called data


def fetch_movie_data(API_key, params):
    all_results = []
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    try:
        for page in range(1, 10):

            params["page"] = page
            response = session.get("https://api.themoviedb.org/3/discover/movie", params=params)
            if response.status_code != 200:
                raise Exception(f"Error fetching data from API: {response.status_code}")

            data = response.json()
            all_results.extend(data.get("results", []))

        logging.info(f"Fetched {len(all_results)} movies from the API")

    except Exception:
        logging.error("Error fetching data from API:", exc_info=True)

    return all_results