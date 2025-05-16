import logging


def transform_movie_data(raw_data, selected_columns):

    primary_data = []
    secondary_data = []

#----------------
    # for loop to iterate through each movie in raw_data

    for movie in raw_data:
        
        # checks if any of the selected columns are missing in the extracted data
        # if missing_columns is not empty it logs an error message with the title of the movie and the missing column(s)

        missing_columns = [key for key in selected_columns if key not in movie]
        if missing_columns:
            logging.error(f"{movie.get("title", "Unknown").upper()} is missing columns: {missing_columns}")

#---------------

        # checks if the movie has a vote count greater than 100 or a vote average of 0.
        # If so, it adds the movie to the secondary_movie
        if movie.get("vote_count", 0) > 400 or movie.get("vote_count", 0) < 75 or movie.get("vote_average", 0) == 0:
            secondary_movie = {key: movie[key] for key in selected_columns if key in movie}
            secondary_data.append(secondary_movie)
            continue
        
        #if the movie passes the above condition it gets added to the primary_data list
        primary_movie = {key: movie[key] for key in selected_columns if key in movie}
        primary_data.append(primary_movie)


    # END OF FOR LOOP
#----------------

    # primary data is sorted by vote_average (highest to lowest)
    # if two movies have the same vote_average it sorts the vote_count (highest to lowest)

    primary_data = sorted(primary_data, key=lambda x: (-x["vote_average"], x["vote_count"]))

    # secondary data is sorted by vote_count (lowest to highest) 
    secondary_data = sorted(secondary_data, key= lambda x: (x["vote_count"], x["vote_average"]))

    logging.info(f"Added to primary_data: {len(primary_data)} movies || Added to secondary_data: {len(secondary_data)} movies")

    return primary_data, secondary_data