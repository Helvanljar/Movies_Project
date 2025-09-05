import json
import os

DATA_FILE = "data.json"

def get_movies():
    """Load and return the movies dictionary from the data file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not read data file. It may be corrupted.")
        return {}

def save_movies(movies):
    """Save the movies dictionary to the data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(movies, f, indent=4)

def add_movie(title, year, rating):
    """Add a new movie to the storage."""
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)

def delete_movie(title):
    """Delete a movie from the storage by its title."""
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)

def update_movie(title, rating):
    """Update the rating of an existing movie."""
    movies = get_movies()
    if title in movies:
        movies[title]['rating'] = rating
        save_movies(movies)
