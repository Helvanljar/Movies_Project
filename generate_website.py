import os
import storage.movie_storage_sql as storage


STATIC_DIR = "_static"
TEMPLATE_FILE = os.path.join(STATIC_DIR, "index_template.html")
OUTPUT_FILE = os.path.join(STATIC_DIR, "index.html")
STYLE_FILE = os.path.join(STATIC_DIR, "style.css")


DEFAULT_TEMPLATE = """<html>
<head>
    <title>My Movie App</title>
    <link rel="stylesheet" href="style.css"/>
</head>
<body>
<div class="list-movies-title">
    <h1>Masterschool's Movie App</h1>
</div>
<div>
    <ol class="movie-grid">
        __TEMPLATE_MOVIE_GRID__
    </ol>
</div>
</body>
</html>
"""

DEFAULT_STYLE = """body {
  background: #F5F5F0;
  color: black;
  font-family: Monaco;
}

.list-movies-title {
  padding: 10px 0;
  background: #009B50;
  color: white;
  text-align: center;
  font-size: 16pt;
}

.movie-grid {
  list-style-type: none;
  padding: 0;
  margin: 0;
  margin-top: 20px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.movie-grid li {
  padding: 10px 15px;
  text-align: left;
}

.movie {
  width: 140px;
}

.movie-title,
.movie-year {
  font-size: 0.8em;
  text-align: center;
}

.movie-title {
  margin-top: 10px;
}

.movie-year {
  color: #999;
}

.movie-poster {
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16),
                0 3px 6px rgba(0, 0, 0, 0.23);
    width: 128px;
    height: 193px;
}
"""


def ensure_static_files():
    """Ensure _static directory and required template/style files exist."""
    os.makedirs(STATIC_DIR, exist_ok=True)

    if not os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_TEMPLATE)

    if not os.path.exists(STYLE_FILE):
        with open(STYLE_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_STYLE)


def generate_movie_grid(movies):
    """Generate HTML grid for all movies."""
    movie_items = []
    for title, data in movies.items():
        poster = data.get("poster_url", "")
        year = data.get("year", "")
        movie_items.append(f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{poster}" title=""/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{year}</div>
            </div>
        </li>
        """)
    return "\n".join(movie_items)


def generate_website():
    """Generate the website (index.html) from template and movies data."""
    ensure_static_files()

    movies = storage.list_movies()
    movie_grid = generate_movie_grid(movies)

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    output = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Website was generated successfully: {OUTPUT_FILE}")
