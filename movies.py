import os
from storage import movie_storage_sql as storage
from generate_website import generate_website

ACTIVE_USER_ID = None


def select_user():
    """Prompt user to select or create a profile."""
    global ACTIVE_USER_ID
    users = storage.list_users()
    print("\nSelect a user:")
    for uid, name in users.items():
        print(f"{uid}. {name}")
    print(f"{len(users) + 1}. Create new user")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("❌ Invalid input.")
        return select_user()

    if choice == len(users) + 1:
        # Prevent empty usernames
        while True:
            name = input("Enter new username: ").strip()
            if not name:
                print("⚠️ Username cannot be empty. Please try again.")
                continue
            ACTIVE_USER_ID = storage.add_user(name)
            print(f"✅ User '{name}' created and selected.")
            break
    elif choice in users:
        ACTIVE_USER_ID = choice
        print(f"🎬 Welcome back, {users[choice]}!")
    else:
        print("❌ Invalid choice.")
        return select_user()


def list_movies():
    """List movies of the active user."""
    movies = storage.list_movies(ACTIVE_USER_ID)
    if not movies:
        print("📢 Your collection is empty.")
        return
    for title, info in movies.items():
        year = info.get("year", "N/A")
        rating = info.get("rating", "N/A")
        print(f"{title} ({year}) ⭐ {rating}")


def add_movie():
    title = input("Enter movie title: ").strip()
    if not title:
        print("⚠️ Title cannot be empty.")
        return
    storage.add_movie_from_api(ACTIVE_USER_ID, title)


def delete_movie():
    title = input("Enter movie title to delete: ").strip()
    if not title:
        print("⚠️ Title cannot be empty.")
        return
    storage.delete_movie(ACTIVE_USER_ID, title)


def update_movie():
    title = input("Enter movie title: ").strip()
    if not title:
        print("⚠️ Title cannot be empty.")
        return
    note = input("Enter note: ").strip()
    storage.update_movie(ACTIVE_USER_ID, title, note)


def stats():
    storage.show_stats(ACTIVE_USER_ID)


def random_movie():
    storage.get_random_movie(ACTIVE_USER_ID)


def search_movie():
    query = input("Enter search term: ").strip()
    if not query:
        print("⚠️ Search term cannot be empty.")
        return
    storage.search_movies(ACTIVE_USER_ID, query)


def movies_sorted_by_rating():
    storage.sort_movies_by_rating(ACTIVE_USER_ID)


def main():
    select_user()
    while True:
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
        choice = input("Enter choice (0-9): ").strip()

        if choice == "0":
            print("👋 Goodbye!")
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
            movies_sorted_by_rating()
        elif choice == "9":
            generate_website()
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
