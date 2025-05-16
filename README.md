# Movie ETL Pipeline Project

This ETL (Extract, Transform, Load) pipeline retrieves movie data from the TMDb API, processes and filters it, and then loads it into a PostgreSQL database and JSON files. The project demonstrates real-world ETL practices, including API integration, data transformation, error handling, logging, and structured database storage.

---

## Project Overview

- **Extract**: Fetches movie data from TMDb API based on genre (e.g., Horror) and release dates (2000–2015).
- **Transform**: 
  - Filters movies into two categories:
    - **Primary Data**: Movies with a vote count between 75 and 400 and a vote average greater than 0.
    - **Secondary Data**: Movies with a vote count less than 75, greater than 400, or a vote average of 0.
  - Handles missing data and logs any issues.
- **Load**: 
  - Saves data to two JSON files (`primary_movies.json`, `secondary_movies.json`).
  - Loads data into two PostgreSQL tables: `primary_movies` and `secondary_movies`.

---

## Technologies Used

- Python 3
- PostgreSQL
- TMDb API
- `psycopg2` (PostgreSQL Integration)
- `requests` (API Calls)
- `dotenv` (Environment Variables)
- `logging` (Application Logging)

---

## Project Structure

<pre> ``` ├── main.py # Entry point for ETL pipeline ├── extract.py # Handles data extraction from API ├── transform.py # Transforms and filters extracted data ├── load.py # Saves data to files and database ├── .env # Stores API keys and database connection info ├── etl_pipeline.log # Log file for monitoring ETL execution └── requirements.txt # Required Python dependencies ``` </pre>



---

## ⚙️ How to Run

1. **Clone the Repository**

```bash
git clone <your-repo-url>
cd <repo-directory>
```


2. **Install dependencies**

```bash
pip install -r requirements
```

3. **Setup Environment Variables**

```
API_KEY=your_tmdb_api_key
DATABASE_URL=your_postgres_connection_url
```

4. **Run the ETL pipeline**

```
python3 main.py
```
