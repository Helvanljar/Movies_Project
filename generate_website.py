import os
from movie_storage_sql import list_movies, get_users

STATIC_DIR = "_static"
HTML_FILE = "index.html"
CSS_FILE = "style.css"
os.makedirs(STATIC_DIR, exist_ok=True)

css_content = """
body {background: #F5F5F0; color: black; font-family: Monaco;}
.list-movies-title {padding: 10px 0; background: #009B50; color: white; text-align: center; font-size: 16pt;}
.movie-grid {list-style: none; display: flex; flex-wrap: wrap; justify-content: center; padding: 0; margin:0;}
.movie-grid li {padding: 10px; text-align:center;}
.movie {width: 140px; margin:5px;}
.movie-title, .movie-year, .movie-rating {font-size: 0.8em;}
.movie-year {color: #999;}
.movie-poster {width:128px; height:193px; box-shadow:0 3px 6px rgba(0,0,0,0.16),0 3px 6px rgba(0,0,0,0.23);}
.movie-poster:hover::after {content: attr(title); position: absolute; background: rgba(0,0,0,0.7); color:white; padding:5px; top:0; left:0; width:140px; font-size:0.7em;}
"""

with open(os.path.join(STATIC_DIR, CSS_FILE), "w", encoding="utf-8") as f:
    f.write(css_content)

# generate all movies for all users
users = get_users()
movie_items = ""
for uid, uname in users.items():
    movies = list_movies(uid)
    if not movies:
        continue
    movie_items += f"<h2>{uname}'s Collection</h2>\n<ol class='movie-grid'>\n"
    for title, info in movies.items():
        country_flag = info['country'][:2].upper() if info['country'] else ""
        note = info['notes'].replace('"', '\\"')
        movie_items += f"""
<li>
    <div class="movie">
        <img class="movie-poster" src="{info['poster_url']}" title="{note}"/>
        <div class="movie-title">{title}</div>
        <div class="movie-year">{info['year']} {country_flag}</div>
        <div class="movie-rating">⭐ {info['rating']}</div>
    </div>
</li>
"""
    movie_items += "</ol>\n"

html_content = f"""<html>
<head>
    <title>Masterschool's Movie App</title>
    <link rel="stylesheet" href="{CSS_FILE}"/>
</head>
<body>
<div class="list-movies-title">
    <h1>Masterschool's Movie App</h1>
</div>
{movie_items}
</body>
</html>"""

with open(os.path.join(STATIC_DIR, HTML_FILE), "w", encoding="utf-8")
