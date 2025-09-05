import os
import requests
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=False)

# Create tables
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """))
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            notes TEXT,
            country TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """))
    conn.commit()


def get_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, username FROM users"))
        return {row[0]: row[1] for row in result.fetchall()}


def add_user(username):
    with engine.connect() as conn:
        try:
            conn.execute(text("INSERT INTO users (username) VALUES (:username)"), {"username": username})
            conn.commit()
            print(f"User '{username}' created.")
        except Exception:
            print(f"User '{username}' already exists.")


def add_movie_from_api(user_id, title):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("Response") == "False":
            print(f"Movie '{title}' not found in OMDb.")
            return

        year = int(data.get("Year", "0")[:4])
        rating = float(data.get("imdbRating", 0))
        poster = data.get("Poster", "")
        country = data.get("Country", "")

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO movies (user_id, title, year, rating, poster_url, notes, country)
                VALUES (:user_id, :title, :year, :rating, :poster_url, '', :country)
            """), {"user_id": user_id, "title": data["Title"], "year": year,
                   "rating": rating, "poster_url": poster, "country": country})
            conn.commit()
            print(f"Movie '{data['Title']}' added successfully for user ID {user_id}.")
    except requests.RequestException:
        print("Could not connect to OMDb API.")


def list_movies(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT title, year, rating, poster_url, notes, country 
            FROM movies WHERE user_id=:user_id
        """), {"user_id": user_id})
        movies = result.fetchall()
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3] or "",
                 "notes": row[4] or "", "country": row[5] or ""}
        for row in movies
    }


def delete_movie(user_id, title):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM movies WHERE user_id=:user_id AND title=:title"),
                     {"user_id": user_id, "title": title})
        conn.commit()


def update_movie(user_id, title, notes):
    with engine.connect() as conn:
        conn.execute(text("UPDATE movies SET notes=:notes WHERE user_id=:user_id AND title=:title"),
                     {"user_id": user_id, "title": title, "notes": notes})
        conn.commit()
        print(f"Movie '{title}' successfully updated.")
