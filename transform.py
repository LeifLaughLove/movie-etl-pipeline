


def transform_movie_data(raw_data, selected_columns):

    transformed_data = []
    print("hello")
    for movie in raw_data["results"]:

        if movie.get("vote_count", 0) > 100 or movie.get("vote_average", 0) == 0:
            continue

        transformed_movie = {key: movie[key] for key in selected_columns if key in movie}
        transformed_data.append(transformed_movie)

    
    transformed_data = sorted(transformed_data, key=lambda x: (-x["vote_average"], x["vote_count"]))
    return transformed_data