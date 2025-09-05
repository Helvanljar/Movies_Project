import movie_storage_sql as storage
import sys
import random
import statistics
import subprocess

ACTIVE_USER_ID = None
ACTIVE_USERNAME = None


def select_user():
    global ACTIVE_USER_ID, ACTIVE_USERNAME
    users = storage.get_users()
    if not users:
        print("No users found. Create a new user:")
        username = input("Enter username: ").strip()
        storage.add_user(username)
        users = storage.get_users()

    print("\nSelect user:")
    for uid, uname in users.items():
        print(f"{uid}. {uname}")
    print("0. Create new user")
    choice = input("Enter choice: ").strip()
    if choice == '0':
        username = input("Enter username: ").strip()
        storage.add_user(username)
        users = storage.get_users()
        ACTIVE_USER_ID = max(users.keys())
        ACTIVE_USERNAME = users[ACTIVE_USER_ID]
    else:
        ACTIVE_USER_ID = int(choice)
        ACTIVE_USERNAME = users[ACTIVE_USER_ID]

    print(f"Welcome, {ACTIVE_USERNAME}!")


def show_menu():
    print("\n********** My Movies Database **********")
    print("Menu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie (Add note)")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Generate website")


def list_movies():
    movies = storage.list_movies(ACTIVE_USER_ID)
    if not movies:
        print(f"{ACTIVE_USERNAME}, your movie collection is empty.")
        return
    for title, info in movies.items():
        note = f" | Note: {info['notes']}" if info['notes'] else ""
        flag = f" ({info['country']})" if info['country'] else ""
        print(f"{title} ({info['year']}){flag}: {info['rating']}{note}")


def add_movie():
    title = input("Enter movie title: ").strip()
    if not title:
        return
    storage.add_movie_from_api(ACTIVE_USER_ID, title)


def delete_movie():
    title = input("Enter movie title to delete: ").strip()
    storage.delete_movie(ACTIVE_USER_ID, title)
    print(f"Deleted '{title}' if it existed.")


def update_movie():
    title = input("Enter movie name: ").strip()
    notes = input("Enter movie note: ").strip()
    storage.update_movie(ACTIVE_USER_ID, title, notes)


def stats():
    movies = storage.list_movies(ACTIVE_USER_ID)
    if not movies:
        print("No movies in your collection.")
        return
    ratings = [info['rating'] for info in movies.values()]
    print(f"Average rating: {statistics.mean(ratings):.1f}")
    print(f"Median rating: {statistics.median(ratings):.1f}")
    best = [t for t, i in movies.items() if i['rating'] == max(ratings)]
    worst = [t for t, i in movies.items() if i['rating'] == min(ratings)]
    print(f"Best movie(s): {best}")
    print(f"Worst movie(s): {worst}")


def random_movie():
    movies = storage.list_movies(ACTIVE_USER_ID)
    if not movies:
        print("No movies in your collection.")
        return
    title = random.choice(list(movies.keys()))
    info = movies[title]
    note = f" | Note: {info['notes']}" if info['notes'] else ""
    print(f"Random movie: {title} ({info['year']}): {info['rating']}{note}")


def search_movie():
    query = input("Enter part of movie name: ").lower()
    movies = storage.list_movies(ACTIVE_USER_ID)
    found = False
    for title, info in movies.items():
        if query in title.lower():
            note = f" | Note: {info['notes']}" if info['notes'] else ""
            print(f"{title} ({info['year']}): {info['rating']}{note}")
            found = True
    if not found:
        print("No matching movies found.")


def sort_movies_by_rating():
    movies = storage.list_movies(ACTIVE_USER_ID)
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, info in sorted_movies:
        note = f" | Note: {info['notes']}" if info['notes'] else ""
        print(f"{title} ({info['year']}): {info['rating']}{note}")


def generate_website():
    import generate_website
    print("Website generated. Exiting now.")
    sys.exit(0)


def main():
    select_user()
    while True:
        show_menu()
        choice = input("Enter choice (0-9): ").strip()
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
            generate_website()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
