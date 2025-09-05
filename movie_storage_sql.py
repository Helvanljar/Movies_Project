from sqlalchemy import create_engine, text

# Database URL
DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=True)

# Drop old table (optional, clears old records)
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS movies"))
    connection.commit()

# Create new movies table with poster URL
with engine.connect() as connection:
    connection.execute(
        text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
        """)
    )
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies")
        )
        movies = result.fetchall()
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }


def add_movie(title, year, rating, poster_url=None):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (title, year, rating, poster_url)
                    VALUES (:title, :year, :rating, :poster_url)
                """),
                {"title": title, "year": year, "rating": rating, "poster_url": poster_url}
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie by title."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()
        if result.rowcount:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")


def update_movie(title, rating):
    """Update the rating of a movie."""
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"title": title, "rating": rating}
        )
        connection.commit()
        if result.rowcount:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")


def get_movies():
    """Alias for list_movies, used in CLI."""
    return list_movies()
