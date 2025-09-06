import os
from storage.movie_storage_sql import list_movies, list_users

STATIC_DIR = "_static"
HTML_FILE = "index.html"
CSS_FILE = "style.css"
os.makedirs(STATIC_DIR, exist_ok=True)

CSS_CONTENT = """
body {background: #F5F5F0; color: black; font-family: Monaco;}
.list-movies-title {padding: 10px 0; background: #009B50; color: white; text-align: center; font-size: 20pt;}
h2 {text-align: center; margin-top: 20px;}
.movie-grid {list-style: none; display: flex; flex-wrap: wrap; justify-content: center; padding: 0; margin:0;}
.movie-grid li {padding: 10px; text-align:center; position: relative;}
.movie {width: 160px; margin:5px;}
.movie-title, .movie-year, .movie-rating {font-size: 0.8em;}
.movie-year {color: #999;}
.movie-poster {width:140px; height:210px; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.3); transition: transform 0.3s;}
.movie-poster:hover {transform: scale(1.05);}
.flag {width: 24px; height: 16px; margin-left: 5px; vertical-align: middle;}
"""

def generate_website():
    with open(os.path.join(STATIC_DIR, CSS_FILE), "w", encoding="utf-8") as f:
        f.write(CSS_CONTENT)

    users = list_users()
    movie_sections = ""
    for uid, uname in users.items():
        movies = list_movies(uid)
        if not movies:
            continue
        movie_sections += f"<h2>{uname}'s Collection</h2>\n<ol class='movie-grid'>\n"
        for title, info in movies.items():
            flag_img = f"<img class='flag' src='https://flagsapi.com/{info['country_code']}/flat/24.png' alt='flag'/>" if info['country_code'] else ""
            note = info['notes'].replace('"', '&quot;') if info['notes'] else ""
            movie_sections += f"""
<li>
    <div class="movie">
        <img class="movie-poster" src="{info['poster_url']}" title="{note}"/>
        <div class="movie-title">{title}</div>
        <div class="movie-year">{info['year']} {flag_img}</div>
        <div class="movie-rating">⭐ {info['rating']}</div>
    </div>
</li>
"""
        movie_sections += "</ol>\n"

    html_content = f"""<html>
<head>
    <title>Masterschool's Movie App</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="{CSS_FILE}"/>
</head>
<body>
<div class="list-movies-title">
    <h1>Masterschool's Movie App</h1>
</div>
{movie_sections}
</body>
</html>"""

    with open(os.path.join(STATIC_DIR, HTML_FILE), "w", encoding="utf-8") as f:
        f.write(html_content)

    print("🌍 Website was generated successfully!")

# Ensure the script runs if executed directly
if __name__ == "__main__":
    generate_website()