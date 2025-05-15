import requests


    # fetch_movie_data function takes the API as an argument and uses the requests library to make a GET request to the API
    # It then converts response to a json file and stores it in a variable called data


def fetch_movie_data(API_key):

    response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={API_key}")
    data = response.json()

    first_movie = data["results"][0]

    print(first_movie)
    print(len(first_movie.keys()))

    return data