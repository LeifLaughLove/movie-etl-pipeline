# Movie ETL Pipeline

A complete ETL (Extract, Transform, Load) pipeline for collecting, cleaning, and analyzing movie data from the TMDb API. This project demonstrates real-world data engineering skills, including API integration, data transformation, database storage, and interactive data exploration via a Python UI.

---

## **Features**

- **Extract:** Fetches movie data from the TMDb API by genre and release date.
- **Transform:** Cleans, filters, and enriches data (genre mapping, rating, streaming provider lookup).
- **Load:** Saves processed data to PostgreSQL and JSON files.
- **UI:** Tkinter-based interface for searching, filtering, and viewing movie details and streaming platforms.
- **SQL Queries:** Includes a `.sql` file with advanced queries for data analysis.
- **Logging & Error Handling:** Tracks ETL process and issues.
- **Secure Credentials:** Uses `.env` for API keys and database URLs.

---

## **Tech Stack**

- Python 3
- PostgreSQL
- TMDb API
- Tkinter (UI)
- psycopg2 (PostgreSQL integration)
- requests (API calls)
- python-dotenv (environment variables)
- logging (application logging)

---

## **Project Structure**

```
├── main.py                # Entry point for ETL pipeline
├── etl/
│   ├── extract.py         # Data extraction from API
│   ├── transform.py       # Data transformation and enrichment
│   ├── load.py            # Save to database and JSON
│   ├── query.py           # SQL query functions
│   ├── config.py          # Configuration (if used)
│   └── movie_etl_queries.sql # Example SQL queries
├── ui/
│   └── app.py             # Tkinter UI for data exploration
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── etl_pipeline.log       # Log file
├── primary_movies.json    # Output JSON (sample)
└── README.md
```

---

## **Setup & Usage**

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/movieETLpipeline.git
    cd movieETLpipeline
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**
    - Create a `.env` file and fill in your TMDb API key and PostgreSQL database URL.

4. **Run the ETL pipeline**
    ```sh
    python3 main.py db
    ```

5. **Launch the UI**
    ```sh
    python3 main.py
    ```

6. **Run SQL queries**
    - Open `etl/movie_etl_queries.sql` in DBeaver or your preferred SQL client.

---
