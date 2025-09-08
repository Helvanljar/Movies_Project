import os
import random
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DB_FILE = os.getenv("DB_FILE", "movies.db")
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

# --- Country mapping ---
COUNTRY_TO_ISO = {
    "United States": "US",
    "United Kingdom": "GB",
    "South Korea": "KR",
    "France": "FR",
    "Germany": "DE",
    "Italy": "IT",
    "Spain": "ES",
    "Japan": "JP",
    "China": "CN",
    "India": "IN",
    "Canada": "CA",
    "Australia": "AU",
}

# --- Database setup ---
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER,
            rating REAL,
            poster_url TEXT,
            notes TEXT,
            country_code TEXT,
            UNIQUE (user_id, title),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """))


# --- User management ---
def list_users():
    """Return a dictionary of user_id -> username."""
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, name FROM users"))
        return {row[0]: row[1] for row in result.fetchall()}


def add_user(name):
    """Add a new user and return its ID."""
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users (name) VALUES (:name)"), {"name": name})
        result = conn.execute(text("SELECT id FROM users WHERE name=:name"), {"name": name})
        return result.scalar()


# --- Movie management ---
def list_movies(user_id):
    """Return a dictionary of title -> movie info for a user."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT title, year, rating, poster_url, notes, country_code
                FROM movies WHERE user_id=:user_id
            """),
            {"user_id": user_id}
        )
        return {
            row[0]: {
                "year": row[1],
                "rating": row[2],
                "poster_url": row[3],
                "notes": row[4],
                "country_code": row[5],
            }
            for row in result.fetchall()
        }


def add_movie_from_api(user_id, title):
    """
    Fetch a movie from OMDb API and add it to the database.
    Avoids duplicates and handles missing API data gracefully.
    """
    # Check for duplicates
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM movies WHERE user_id=:uid AND title=:title"),
            {"uid": user_id, "title": title}
        ).fetchone()
        if exists:
            print(f"⚠️ Movie '{title}' already exists in your collection.")
            return

    api_key = os.getenv("OMDB_API_KEY")
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception:
        print("❌ Failed to fetch movie data from OMDb.")
        return

    if data.get("Response") == "False":
        print(f"❌ Movie '{title}' not found in OMDb.")
        return

    # Fallbacks for missing fields
    year = None
    if data.get("Year") and data["Year"] != "N/A":
        year = int(data["Year"].split("–")[0])

    rating = 0.0
    if data.get("imdbRating") and data["imdbRating"] != "N/A":
        try:
            rating = float(data["imdbRating"])
        except ValueError:
            rating = 0.0

    poster = data.get("Poster") if data.get("Poster") and data["Poster"] != "N/A" else ""

    country_full = ""
    country_code = "UN"
    if data.get("Country") and data["Country"] != "N/A":
        country_full = data["Country"].split(",")[0].strip()
        country_code = COUNTRY_TO_ISO.get(country_full, "UN")

    # Insert into database
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO movies (user_id, title, year, rating, poster_url, notes, country_code)
                VALUES (:user_id, :title, :year, :rating, :poster_url, '', :country_code)
            """),
            {
                "user_id": user_id,
                "title": data.get("Title", title),
                "year": year,
                "rating": rating,
                "poster_url": poster,
                "country_code": country_code,
            }
        )

    print(f"✅ Movie '{title}' added with country {country_full or 'Unknown'} ({country_code})")


def delete_movie(user_id, title):
    """Delete a movie, verifying it exists first."""
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM movies WHERE user_id=:uid AND title=:title"),
            {"uid": user_id, "title": title}
        ).fetchone()
        if not exists:
            print(f"❌ Movie '{title}' not found in your collection.")
            return

        conn.execute(
            text("DELETE FROM movies WHERE user_id=:uid AND title=:title"),
            {"uid": user_id, "title": title}
        )

    print(f"🗑️ Movie '{title}' deleted.")


def update_movie(user_id, title, note):
    """Update a movie's note, verifying it exists first."""
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM movies WHERE user_id=:uid AND title=:title"),
            {"uid": user_id, "title": title}
        ).fetchone()
        if not exists:
            print(f"❌ Movie '{title}' not found in your collection.")
            return

        conn.execute(
            text("UPDATE movies SET notes=:note WHERE user_id=:uid AND title=:title"),
            {"note": note, "uid": user_id, "title": title}
        )

    print(f"📝 Movie '{title}' updated with note.")


def show_stats(user_id):
    """Print number of movies and average rating for a user."""
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT COUNT(*), AVG(rating) FROM movies WHERE user_id=:uid"),
            {"uid": user_id}
        )
        count, avg = result.fetchone()
        if count:
            print(f"🎥 {count} movies, average rating {avg:.1f}")
        else:
            print("No movies.")


def get_random_movie(user_id):
    """Pick and display a random movie for a user."""
    movies = list_movies(user_id)
    if not movies:
        print("📢 No movies available.")
        return
    title = random.choice(list(movies.keys()))
    print(f"🎲 Random pick: {title} ({movies[title]['year']})")


def search_movies(user_id, query):
    """Search for movies by title substring (case-insensitive)."""
    movies = list_movies(user_id)
    found = [t for t in movies if query.lower() in t.lower()]
    if not found:
        print("❌ No match found.")
    else:
        for t in found:
            print(f"🔎 {t} ({movies[t]['year']})")


def sort_movies_by_rating(user_id):
    """List movies sorted by rating, highest first."""
    movies = list_movies(user_id)
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ⭐ {info['rating']}")
