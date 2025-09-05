import os
import random
import statistics
import requests
from dotenv import load_dotenv
import movie_storage_sql as storage

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def show_menu():
    """Display the menu."""
    print("\n********** My Movies Database **********")
    print("Menu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Generate website")


def list_movies():
    """Display all movies."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def add_movie():
    """Add a movie via OMDb API."""
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "False":
            print(f"Movie not found: {data.get('Error')}")
            return
        year = int(data.get("Year", 0))
        rating = float(data.get("imdbRating", 0.0))
        poster = data.get("Poster", "")
        storage.add_movie(data["Title"], year, rating, poster)
        print(f"Movie '{data['Title']}' added successfully.")
    except requests.RequestException as e:
        print(f"Error accessing API: {e}")


def delete_movie():
    """Delete a movie from the database."""
    title = input("Enter movie name to delete: ").strip()
    storage.delete_movie(title)
    print(f"Deleted '{title}' if it existed.")


def update_movie():
    """Update a movie rating in the database."""
    title = input("Enter movie name to update rating: ").strip()
    try:
        rating = float(input("Enter new rating (1-10): "))
        if rating < 1 or rating > 10:
            print("Rating must be 1-10.")
            return
        storage.update_movie(title, rating)
        print(f"Updated '{title}' to rating {rating}.")
    except ValueError:
        print("Invalid input.")


def stats():
    """Show statistics of movies."""
    movies = storage.list_movies()
    if not movies:
        print("No movies.")
        return
    ratings = [info["rating"] for info in movies.values()]
    avg = statistics.mean(ratings)
    med = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)
    best = [t for t, i in movies.items() if i["rating"] == max_rating]
    worst = [t for t, i in movies.items() if i["rating"] == min_rating]
    print(f"Average rating: {avg:.1f}")
    print(f"Median rating: {med:.1f}")
    print(f"Best: {best}")
    print(f"Worst: {worst}")


def random_movie():
    """Show a random movie."""
    movies = storage.list_movies()
    if not movies:
        print("No movies.")
        return
    title = random.choice(list(movies.keys()))
    info = movies[title]
    print(f"Random movie: {title} ({info['year']}): {info['rating']}")


def search_movie():
    """Search movies by name."""
    movies = storage.list_movies()
    query = input("Enter part of movie name: ").lower()
    found = False
    for title, info in movies.items():
        if query in title.lower():
            print(f"{title} ({info['year']}): {info['rating']}")
            found = True
    if not found:
        print("No matches found.")


def sort_movies_by_rating():
    """Sort movies by rating descending."""
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")


def main():
    """Main program loop."""
    while True:
        show_menu()
        choice = input("Enter choice (0-9): ").strip()
        if choice == "0":
            print("Bye!")
            break
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            sort_movies_by_rating()
        elif choice == "9":
            import generate_website
            generate_website.generate_website()
            print("Website generated. Exiting.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
