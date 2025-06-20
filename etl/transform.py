from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import requests


def transform_movie_data(API_key, raw_data, selected_columns):
    primary_data = []
    certification_cache = {}
    allowed_ratings = {"G", "PG", "PG-13", "R"}
    genre_mapping = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    # Create a dictionary of valid movies with ID (not adult and has ID)
    movie_id_map = {movie["id"]: movie for movie in raw_data if movie.get("id")}

    # Fetch certifications in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(filter_movie_certification, movie_id, API_key): movie_id for movie_id in movie_id_map}
        for future in as_completed(future_to_id):
            movie_id = future_to_id[future]
            try:
                cert = future.result()
                certification_cache[movie_id] = cert
            except Exception as e:
                logging.error(f"Error fetching cert for movie ID {movie_id}: {e}")
                certification_cache[movie_id] = None

    # Process movies
    for movie_id, movie in movie_id_map.items():
        cert = certification_cache.get(movie_id)
        if cert not in allowed_ratings:
            continue

        # Check for missing columns
        missing_columns = [key for key in selected_columns if key not in movie]
        if missing_columns:
            logging.error(f"{movie.get('title', 'Unknown').upper()} is missing columns: {missing_columns}")

        movie_data = {key: movie[key] for key in selected_columns if key in movie}


        genre_ids = movie_data.get("genre_ids", [])
        genre_names = [genre_mapping.get(gid, "Unknown") for gid in genre_ids]
    

        movie_data["rating"] = cert
        movie_data["genres"] = ", ".join(genre_names)

        
        primary_data.append(movie_data)

    # Sort results
    primary_data = sorted(primary_data, key=lambda x: (-x["vote_average"], x["vote_count"]))

    logging.info(f"Added to primary_data: {len(primary_data)} movies")
    return primary_data


#filter movie certification runs to check the rating of each movie
#           when the API is called the list of movies returned does not have rating [G, PG, PG-13...] as a key,value 
#           calling the API again for each movie along with the integration of ThreadPoolExecutor 
#           allows up to 10 calls be made at once to the API making it significantly faster

def filter_movie_certification(movie_id, API_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"
    response = requests.get(url, params={"api_key": API_key})
    if response.status_code != 200:
        return None

    data = response.json()
    for entry in data.get("results", []):
        if entry.get("iso_3166_1") == "US":
            for release in entry.get("release_dates", []):
                cert = release.get("certification")
                if cert:
                    return cert
    return None