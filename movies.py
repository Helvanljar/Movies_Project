import os
import json
import movie_storage
import statistics
import random

DATA_FILE = "data.json"

# Create empty data.json file if it does not exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

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
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return
    print(f"\n{len(movies)} movie(s) in total:")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")

def add_movie():
    """Add a new movie with title, year, and rating."""
    movies = movie_storage.get_movies()
    while True:
        title = input("Enter movie name: ").strip()
        if not title:
            print("Movie title cannot be empty. Please try again.")
            continue
        if title in movies:
            print("Movie already exists.")
            return
        break

    while True:
        try:
            year = int(input("Enter movie year: "))
            break
        except ValueError:
            print("Invalid year. Please enter a valid number.")

    while True:
        try:
            rating = float(input("Enter movie rating (1-10): "))
            if rating < 1 or rating > 10:
                print("Rating must be between 1 and 10.")
                continue
            break
        except ValueError:
            print("Invalid rating. Please enter a number between 1 and 10.")

    movie_storage.add_movie(title, year, rating)
    print(f"Added '{title}' ({year}) with rating {rating}.")

def delete_movie():
    """Delete a movie by its title."""
    movies = movie_storage.get_movies()
    title = input("Enter movie name to delete: ").strip()
    if title in movies:
        movie_storage.delete_movie(title)
        print(f"Deleted '{title}'.")
    else:
        print("Movie not found.")

def update_movie():
    """Update the rating of an existing movie."""
    movies = movie_storage.get_movies()
    title = input("Enter movie name to update: ").strip()
    if title in movies:
        while True:
            try:
                rating = float(input("Enter new rating (1-10): "))
                if rating < 1 or rating > 10:
                    print("Rating must be between 1 and 10.")
                    continue
                break
            except ValueError:
                print("Invalid rating. Please enter a number between 1 and 10.")
        movie_storage.update_movie(title, rating)
        print(f"Updated '{title}' to rating {rating}.")
    else:
        print("Movie not found.")

def stats():
    """Show statistics including average, median, best and worst movies."""
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return
    ratings = [info['rating'] for info in movies.values()]
    avg = statistics.mean(ratings)
    med = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)

    best_movies = [title for title, info in movies.items() if info['rating'] == max_rating]
    worst_movies = [title for title, info in movies.items() if info['rating'] == min_rating]

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
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return
    title = random.choice(list(movies.keys()))
    info = movies[title]
    print(f"\nRandom movie: {title} ({info['year']}): {info['rating']}")

def search_movie():
    """Search for movies by partial name match."""
    movies = movie_storage.get_movies()
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
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    print("\nMovies sorted by rating (highest to lowest):")
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")

def sort_movies_by_year():
    """Sort and display movies by year."""
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    while True:
        choice = input("Show latest movies first? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    reverse = choice == 'y'
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=reverse)
    print("\nMovies sorted by year:")
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")

def filter_movies():
    """Filter movies by minimum rating and year range."""
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in the database.")
        return

    while True:
        min_rating = input("Enter minimum rating (leave blank for no minimum rating): ").strip()
        if min_rating == "" or min_rating.replace('.', '', 1).isdigit():
            break
        print("Invalid minimum rating. Please enter a number or leave blank.")

    while True:
        start_year = input("Enter start year (leave blank for no start year): ").strip()
        if start_year == "" or start_year.isdigit():
            break
        print("Invalid start year. Please enter a valid year or leave blank.")

    while True:
        end_year = input("Enter end year (leave blank for no end year): ").strip()
        if end_year == "" or end_year.isdigit():
            break
        print("Invalid end year. Please enter a valid year or leave blank.")

    min_rating_val = float(min_rating) if min_rating else None
    start_year_val = int(start_year) if start_year else None
    end_year_val = int(end_year) if end_year else None

    filtered = {
        title: info
        for title, info in movies.items()
        if (min_rating_val is None or info['rating'] >= min_rating_val) and
           (start_year_val is None or info['year'] >= start_year_val) and
           (end_year_val is None or info['year'] <= end_year_val)
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
        if choice == '0':
            print("Bye!")
            break
        elif choice == '1':
            list_movies()
        elif choice == '2':
            add_movie()
        elif choice == '3':
            delete_movie()
        elif choice == '4':
            update_movie()
        elif choice == '5':
            stats()
        elif choice == '6':
            random_movie()
        elif choice == '7':
            search_movie()
        elif choice == '8':
            sort_movies_by_rating()
        elif choice == '9':
            sort_movies_by_year()
        elif choice == '10':
            filter_movies()
        else:
            print("Invalid choice. Please enter a number from 0 to 10.")

if __name__ == "__main__":
    main()
