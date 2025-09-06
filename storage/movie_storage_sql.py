import os
import random
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import requests

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
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """))


# --- User management ---
def list_users():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id, name FROM users"))
        return {row[0]: row[1] for row in result.fetchall()}


def add_user(name):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users (name) VALUES (:name)"), {"name": name})
        result = conn.execute(text("SELECT id FROM users WHERE name=:name"), {"name": name})
        return result.scalar()


# --- Movie management ---
def list_movies(user_id):
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT title, year, rating, poster_url, notes, country_code
            FROM movies WHERE user_id=:user_id
        """), {"user_id": user_id})
        return {
            row[0]: {
                "year": row[1],
                "rating": row[2],
                "poster_url": row[3],
                "notes": row[4],
                "country_code": row[5],
            } for row in result.fetchall()
        }


def add_movie_from_api(user_id, title):
    api_key = os.getenv("OMDB_API_KEY")
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data.get("Response") == "False":
        print(f"❌ Movie '{title}' not found in OMDb.")
        return

    year = int(data.get("Year", "0").split("–")[0]) if data.get("Year") else None
    rating = float(data.get("imdbRating", 0.0)) if data.get("imdbRating") != "N/A" else 0.0
    poster = data.get("Poster") if data.get("Poster") != "N/A" else ""

    country_full = data.get("Country", "").split(",")[0].strip()
    country_code = COUNTRY_TO_ISO.get(country_full, "UN")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO movies (user_id, title, year, rating, poster_url, notes, country_code)
            VALUES (:user_id, :title, :year, :rating, :poster_url, '', :country_code)
        """), {
            "user_id": user_id,
            "title": data["Title"],
            "year": year,
            "rating": rating,
            "poster_url": poster,
            "country_code": country_code,
        })

    print(f"✅ Movie '{title}' added with country {country_full} ({country_code})")


def delete_movie(user_id, title):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM movies WHERE user_id=:uid AND title=:title"),
                     {"uid": user_id, "title": title})
    print(f"🗑️ Movie '{title}' deleted.")


def update_movie(user_id, title, note):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE movies SET notes=:note WHERE user_id=:uid AND title=:title
        """), {"note": note, "uid": user_id, "title": title})
    print(f"📝 Movie '{title}' updated with note.")


def show_stats(user_id):
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*), AVG(rating) FROM movies WHERE user_id=:uid
        """), {"uid": user_id})
        count, avg = result.fetchone()
        print(f"🎥 {count} movies, average rating {avg:.1f}" if count else "No movies.")


def get_random_movie(user_id):
    movies = list_movies(user_id)
    if not movies:
        print("📢 No movies available.")
        return
    title = random.choice(list(movies.keys()))
    print(f"🎲 Random pick: {title} ({movies[title]['year']})")


def search_movies(user_id, query):
    movies = list_movies(user_id)
    found = [t for t in movies if query.lower() in t.lower()]
    if not found:
        print("❌ No match found.")
    else:
        for t in found:
            print(f"🔎 {t} ({movies[t]['year']})")


def sort_movies_by_rating(user_id):
    movies = list_movies(user_id)
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ⭐ {info['rating']}")
