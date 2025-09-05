import sys
import random
import storage.movie_storage_sql as storage


def list_movies():
    """List all movies in the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies found.")
        return
    print(f"\n{len(movies)} movies in total:\n")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def add_movie():
    """Add a new movie by fetching from OMDb API."""
    title = input("Enter movie title: ")
    storage.add_movie(title)


def delete_movie():
    """Delete a movie by title."""
    title = input("Enter movie title to delete: ")
    storage.delete_movie(title)


def update_movie():
    """Update a movie’s rating manually (not used much with API)."""
    title = input("Enter movie title to update: ")
    try:
        rating = float(input("Enter new rating: "))
        storage.update_movie(title, rating)
    except ValueError:
        print("Invalid rating. Please enter a number.")


def stats():
    """Show statistics: average, median, best, worst movies."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available for statistics.")
        return

    ratings = [data["rating"] for data in movies.values()]
    avg = sum(ratings) / len(ratings)
    median = sorted(ratings)[len(ratings) // 2]

    best_movie = max(movies, key=lambda t: movies[t]["rating"])
    worst_movie = min(movies, key=lambda t: movies[t]["rating"])

    print(f"Average rating: {avg:.2f}")
    print(f"Median rating: {median:.1f}")
    print(f"Best movie: {best_movie} ({movies[best_movie]['rating']})")
    print(f"Worst movie: {worst_movie} ({movies[worst_movie]['rating']})")


def random_movie():
    """Pick and display a random movie."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    movie = random.choice(list(movies.keys()))
    print(f"Your random movie: {movie} ({movies[movie]['year']}): {movies[movie]['rating']}")


def search_movie():
    """Search for movies containing a substring in the title."""
    movies = storage.list_movies()
    query = input("Enter search term: ").lower()
    results = {t: d for t, d in movies.items() if query in t.lower()}
    if results:
        for title, data in results.items():
            print(f"{title} ({data['year']}): {data['rating']}")
    else:
        print("No results found.")


def movies_sorted_by_rating():
    """List all movies sorted by rating, descending."""
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def print_menu():
    """Display the menu options."""
    print("""
Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
""")


def main():
    """Main function for CLI."""
    while True:
        print_menu()
        choice = input("Enter choice (0-9): ")

        if choice == "0":
            print("Bye!")
            sys.exit()
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
            movies_sorted_by_rating()
        elif choice == "9":
            import website_generator
            website_generator.generate_website()
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
