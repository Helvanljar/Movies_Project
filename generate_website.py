import os
import movie_storage_sql as storage

TEMPLATE_HTML = """<html>
<head>
    <title>Masterschool's Movie App</title>
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

CSS_CONTENT = """
body {
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
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
    width: 128px;
    height: 193px;
}
"""


def generate_website():
    movies = storage.list_movies()
    movie_items = ""
    for title, info in movies.items():
        poster = info.get("poster_url") or ""
        movie_items += f"""        <li>
            <div class="movie">
                <img class="movie-poster" src="{poster}" title=""/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info['year']}</div>
            </div>
        </li>\n"""
    html_content = TEMPLATE_HTML.replace("__TEMPLATE_MOVIE_GRID__", movie_items)

    if not os.path.exists("_static"):
        os.makedirs("_static")

    with open("_static/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("_static/style.css", "w", encoding="utf-8") as f:
        f.write(CSS_CONTENT)

    print("Website was generated successfully.")
