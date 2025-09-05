import random
import statistics
import requests
import movie_storage_sql as storage  # SQL-backed storage

# ---------------------- OMDb API Config ----------------------
API_KEY = "YOUR_OMDB_API_KEY"  # Replace with your API key
BASE_URL = "http://www.omdbapi.com/"


def fetch_movie_data(title):
    """
    Fetch movie information from OMDb API by title.
    Returns a dictionary with title, year, rating, and actors.
    """
    params = {"apikey": API_KEY, "t": title}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("Error: Could not connect to OMDb API.")
        return None

    data = response.json()
    if data.get("Response") == "False":
        print(f"Movie not found: {title}")
        return None

    movie_info = {
        "title": data.get("Title"),
        "year": int(data.get("Year", 0)),
        "rating": float(data.get("imdbRating")) if data.get("imdbRating") != "N/A" else 0.0,
        "actors": data.get("Actors", "").split(", ")
    }
    return movie_info

# ---------------------- CLI Functions ----------------------
def show_menu():
    """Display the main menu options."""
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
    print("9. Movies sorted by year")
    print("10. Filter movies")


def list_movies():
    """List all movies in the database."""
    movies = storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return
    print(f"\n{len(movies)} movie(s) in total:")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def add_movie():
    """Add a new movie by fetching details from OMDb API."""
    title = input("Enter movie name: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    movie_info = fetch_movie_data(title)
    if movie_info is None:
        return

    storage.add_movie(movie_info["title"], movie_info["year"], movie_info["rating"])
    print(f"Added '{movie_info['title']}' ({movie_info['year']}) with rating {movie_info['rating']}.")
    print(f"Actors: {', '.join(movie_info['actors'])}")


def delete_movie():
    """Delete a movie by its title."""
    title = input("Enter movie name to delete: ").strip()
    storage.delete_movie(title)


def update_movie():
    """Update the rating of an existing movie."""
    title = input("Enter movie name to update: ").strip()
    while True:
        try:
            rating = float(input("Enter new rating (1-10): "))
            if 1 <= rating <= 10:
                break
            print("Rating must be between 1 and 10.")
        except ValueError:
            print("Invalid rating. Enter a number between 1 and 10.")

    storage.update_movie(title, rating)


def stats():
    """Show statistics including average, median, best, and worst movies."""
    movies = storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    ratings = [info["rating"] for info in movies.values()]
    avg = statistics.mean(ratings)
    med = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)

    best_movies = [t for t, i in movies.items() if i["rating"] == max_rating]
    worst_movies = [t for t, i in movies.items() if i["rating"] == min_rating]

    print(f"\nAverage rating: {avg:.1f}")
    print(f"Median rating: {med:.1f}")
    print("Best movie(s):")
    for title in best_movies:
        print(f"{title}: {max_rating}")
    print("Worst movie(s):")
    for title in worst_movies:
        print(f"{title}: {min_rating}")


def random_movie():
    """Show a random movie from the database."""
    movies = storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    title = random.choice(list(movies.keys()))
    info = movies[title]
    print(f"\nRandom movie: {title} ({info['year']}): {info['rating']}")


def search_movie():
    """Search for movies by partial name match."""
    movies = storage.get_movies()
    query = input("Enter part of movie name: ").lower()
    found = False
    for title, info in movies.items():
        if query in title.lower():
            print(f"{title} ({info['year']}): {info['rating']}")
            found = True
    if not found:
        print("No matching movies found.")


def sort_movies_by_rating():
    """Sort and display movies by rating in descending order."""
    movies = storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    sorted_movies = sorted(
        movies.items(), key=lambda x: x[1]["rating"], reverse=True
    )
    print("\nMovies sorted by rating (highest to lowest):")
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")


def sort_movies_by_year():
    """Sort and display movies by year."""
    movies = storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    while True:
        choice = input("Show latest movies first? (y/n): ").strip().lower()
        if choice in ["y", "n"]:
            break
        print("Invalid input. Enter 'y' or 'n'.")

    reverse = choice == "y"
    sorted_movies = sorted(
        movies.items(), key=lambda x: x[1]["year"], reverse=reverse
    )
    print("\nMovies sorted by year:")
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")


def filter_movies():
    """Filter movies by minimum rating and year range."""
    movies = storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    while True:
        min_rating = input(
            "Enter minimum rating (leave blank for no minimum rating): "
        ).strip()
        if min_rating == "" or min_rating.replace(".", "", 1).isdigit():
            break
        print("Invalid minimum rating.")

    while True:
        start_year = input(
            "Enter start year (leave blank for no start year): "
        ).strip()
        if start_year == "" or start_year.isdigit():
            break
        print("Invalid start year.")

    while True:
        end_year = input("Enter end year (leave blank for no end year): ").strip()
        if end_year == "" or end_year.isdigit():
            break
        print("Invalid end year.")

    min_rating_val = float(min_rating) if min_rating else None
    start_year_val = int(start_year) if start_year else None
    end_year_val = int(end_year) if end_year else None

    filtered = {
        t: i
        for t, i in movies.items()
        if (min_rating_val is None or i["rating"] >= min_rating_val)
        and (start_year_val is None or i["year"] >= start_year_val)
        and (end_year_val is None or i["year"] <= end_year_val)
    }

    if not filtered:
        print("No movies match the filter criteria.")
        return

    print("\nFiltered Movies:")
    for title, info in filtered.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def main():
    """Main loop to run the menu-driven movie manager."""
    while True:
        show_menu()
        choice = input("Enter choice (0-10): ").strip()
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
            sort_movies_by_year()
        elif choice == "10":
            filter_movies()
        else:
            print("Invalid choice. Enter a number from 0 to 10.")


if __name__ == "__main__":
    main()
