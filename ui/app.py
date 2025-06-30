import logging
import os
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import requests

from etl.query import fetch_movies_from_db

# APP.PY LAUNCHES THE UI TO ALLOW USERS TO EASILY SEARCH THROUGH MOVIES, ALLOWING TO FITLER BY RATING, GENRE, AND RELEASE DATE.
# CAN SORT BY TITLE ASC-DESC AND RATING ASC-DESC

def launch_ui():
                    #ON SEARCH FUNCION RUN WHEN USER PRESSES THE SEARCH BUTTON
    def on_search():
      
        selected_sort = sort_var.get()
        min_year = min_year_dropdown.get()
        max_year = max_year_dropdown.get()
        genre = genre_dropdown.get()
        rating = rating_dropdown.get()

        if selected_sort == "title_az":
            order = "ASC"
            selected_sort = "title"
        elif selected_sort == "title_za":
            order = "DESC"
            selected_sort = "title"
        elif selected_sort == "vote_avg_high_low":
            order = "DESC"
            selected_sort = "vote_average"
        elif selected_sort == "vote_avg_low_high":
            order = "ASC"
            selected_sort = "vote_average"

        print("Sort by:", selected_sort)
        print(min_year, max_year, genre)
        movies = fetch_movies_from_db(selected_sort, min_year, max_year, genre, rating, order)


        for row in tree.get_children():
            tree.delete(row)
        for movie in movies:
            tree.insert("", tk.END, values=(
                movie['tmdb_id'],
                movie['title'], 
                movie['rating'], 
                movie['vote_average'], 
                movie['genres'], 
                movie['release_date']))



    window = tk.Tk()
    window.title("ETL Pipeline Dashboard")
    window.geometry("1000x800")

    btn = tk.Button(window, text="SEARCH", command=on_search)
    btn.grid(row=2, column=8, padx=5, pady=2)

    welcome_text = tk.Label(window, text="Movie Finder", width=20, font=("Arial", 12, "bold"))
    welcome_text.grid(row=1, column=4, columnspan=3, padx=0, pady=0)

    

    #RATING DROPDOWN MENU EXAMPLE "G, PG, PG-13..."
    rating_label = tk.Label(window, text="Rating:", width=6, font=("Arial", 10, "bold"))
    rating_label.grid(row=5, column=3, padx=0, pady=0)
    rating_var = tk.StringVar()

    rating_dropdown = ttk.Combobox(window, textvariable=rating_var, width=5)
    rating_dropdown['values'] = ("Any", 'G', 'PG', 'PG-13', 'R')
    rating_dropdown.current(2)
    rating_dropdown.grid(row=6, column=3, padx=0, pady=0)

# MIN & MAX YEAR DROPDOWN SELECTION. -------------------------------------------------------------------
# ALSO CONTAINS A FUNCTION TO UPDATE THE MAX YEAR SELECTION BASED OFF OF THE SELECTED MIN YEAR SELECTION

    year_selection_label = tk.Label(window, text="Date Selection", width=12, font=("Arial", 10, "bold"))
    year_selection_label.grid(row=5,column=5, columnspan=3)

    min_years = list(map(str, range(1965, 2025)))
    min_year_dropdown = ttk.Combobox(window, width=5)
    min_year_dropdown['values'] = min_years
    min_year_dropdown.current(0)
    min_year_dropdown.grid(row=6, column=5, padx=5, pady=0, sticky="e")


    between_dates_label = tk.Label(window, text="TO", width=5, font=("Arial", 8, "bold"))
    between_dates_label.grid(row=6, column=6, padx=0, pady=0)

    max_years = list(map(str, range(int(min_year_dropdown.get()), 2026)))
    max_year_dropdown = ttk.Combobox(window, width=5)
    max_year_dropdown['values'] = max_years
    max_year_dropdown.current(len(max_years) - 1)
    max_year_dropdown.grid(row=6, column=7, padx=0, pady=0, sticky="w")

    def update_max_years(event=None):
        min_year = int(min_year_dropdown.get())
        max_years = list(map(str, range(min_year + 1, 2026)))
        max_year_dropdown['values'] = max_years
        if max_years:
            max_year_dropdown.current(len(max_years) -1)
        else:
            max_year_dropdown.set("")

    min_year_dropdown.bind("<<ComboboxSelected>>", update_max_years)
    update_max_years()
#--------------------------------------
# GENRE DROPDOWN ----------------------

    genre_label = tk.Label(window, text="Genre", width=5, font=("Arial", 10, "bold"))
    genre_label.grid(row=5, column=4, padx=0, pady=0)


    genre_dropdown = ttk.Combobox(window, width=10)
    genre_dropdown['values'] = ("Any", "Action", "Horror", "Comedy")
    genre_dropdown.current(0)
    genre_dropdown.grid(row=6, column=4)

#---------------------------------------
# SORT BY ------------------------------

    sort_var = tk.StringVar(value="title_az")

    tk.Label(window, text="Sort By:",).grid(row=2,column=1)

    tk.Radiobutton(window, text="Title A-Z",variable=sort_var, value="title_az").grid(row=3,column=1, sticky="w")
    tk.Radiobutton(window, text="Title Z-A",variable=sort_var, value="title_za").grid(row=4,column=1, sticky="w")
    tk.Radiobutton(window, text="Vote Average High-Low",variable=sort_var, value="vote_avg_high_low").grid(row=5,column=1, sticky="w")
    tk.Radiobutton(window, text="Vote Average Low-High",variable=sort_var, value="vote_avg_low_high").grid(row=6,column=1, sticky="w")

#---------------------------------------
# RESULTS WINDOW PANE LOGIC -------------

    results_frame = tk.Frame(window)
    results_frame.grid(row=7, column=1, columnspan=12, rowspan=30, sticky="nsew")

        # Define columns
    columns = ("tmdb_id","title", "rating", "vote_average", "genres", "release_date")
    tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=20)

    # Define headings, tree heading is seperate because it's not shown to the user
    tree.heading("tmdb_id", text="TMDB ID")

    tree.heading("title", text="Title")
    tree.heading("rating", text="Rating")
    tree.heading("vote_average", text="Vote Average")
    tree.heading("genres", text="Genres")
    tree.heading("release_date", text="Release Date")

    # tree column width=0 so that users are not shown tmdb_id
    tree.column("tmdb_id", width=0, stretch=False)

    tree.column("title", width=300)
    tree.column("rating", width=60)
    tree.column("vote_average", width=100)
    tree.column("genres", width=200)
    tree.column("release_date", width=150)

    # Add vertical scrollbar
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



#-------------------------------------------------------------------------------------------
# CURRENT MOVIE INFORMATION 
# on_tree_selection RUNS WHEN USER SLEECTS A MOVIE FROM THE LIST. 
# IT SHOWS THE MOVIE INFORMATION TO THE USER BELOW THE LIST OF MOVIES. 
# IT ALSO CALLS THE MOVIEDB PROVIDERS HTTP TO FIND OUT WHERE THE SELECTED MOVIE IS STREAMING

    movie_info = tk.Label(window, text="HELLO", justify="left", anchor="w", wraplength=800)
    movie_info.grid(row=38, column=1, columnspan=12, sticky="w", padx=10)


    def on_tree_selection(event):
        selected = tree.selection()

        load_dotenv()
        API_KEY = os.getenv("API_KEY")

        
        providers = []


        if selected:
            item = tree.item(selected[0])
            values = item['values']
            tmdb_id = values[0]

            url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers"
            response = requests.get(url, params={"api_key": API_KEY})
            data = response.json()

            title = values[1]
            rating = values[2]
            vote_average = values[3]
            genres = values[4]
            release_date = values[5]
            

            try:
                for provider in data["results"]["US"]["flatrate"]:
                    providers.append(provider["provider_name"])
                    logging.info(f"Streaming providers fetched successfully {values[1]}")
            except Exception:
                logging.error(f"Error fetching movie provider from API:\nMovie Title: {values[1]}", exc_info=True)
                providers.append("No Streaming information for this movie")


            info_text = f"Title: {title}\nRating: {rating}\nVote Average: {vote_average}\nGenres: {genres}\nRelease Date: {release_date}\nProviders: {', '.join(providers)}"
            movie_info.config(text=info_text)

    tree.bind("<<TreeviewSelect>>", on_tree_selection)


   # window.grid_columnconfigure(1, weight=1)

    window.mainloop()



    

