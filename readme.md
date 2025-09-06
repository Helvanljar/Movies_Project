# 🎬 Masterschool's Movie App

A Python-based application to manage your movie collection, fetch metadata from the OMDb API, and generate a visually appealing static HTML website showcasing movie posters, ratings, and country flags.

## ✨ Features
- **Multi-user support**: Manage movie collections for multiple user profiles.
- **OMDb API integration**: Automatically fetch movie details (title, year, rating, poster, country).
- **Country flags**: Display country-specific flags using [FlagsAPI](https://flagsapi.com/).
- **SQLite database**: Store movie data persistently using SQLAlchemy.
- **Static website generation**: Create a responsive HTML website with hover effects on movie posters, ratings (⭐), and notes.
- **Interactive CLI**: Add, delete, update, search, sort, and view stats for movies.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Helvanljar/movies_project.git
   cd movies_project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with the following:
   ```env
   OMDB_API_KEY=your_api_key_here
   DB_FILE=movies.db
   ```
   Obtain a free OMDb API key from [OMDb API](http://www.omdbapi.com/apikey.aspx).

## ▶️ Usage

Run the main program:
```bash
python movies.py
```

### Available Commands
- `1` - List all movies in your collection.
- `2` - Add a movie (fetched automatically via OMDb API).
- `3` - Delete a movie.
- `4` - Update a movie's note.
- `5` - View collection stats.
- `6` - Pick a random movie.
- `7` - Search movies by title.
- `8` - Sort movies by rating.
- `9` - Generate a static website.

### 🌍 Generated Website
Running option `9` generates a static website in:
```
movies_project/_static/index.html
```
Open `index.html` in a browser to view your movie collection with:
- Movie posters with hover effects.
- Titles, release years, and ratings (e.g., ⭐ 8.5).
- Country flags for each movie.
- User-specific collections grouped by profile.

To serve the website locally for testing:
```bash
cd _static
python -m http.server
```
Visit `http://localhost:8000` in your browser.

## 📋 Prerequisites
- **Python**: 3.9 or higher
- **Dependencies** (listed in `requirements.txt`):
  - `requests`
  - `sqlalchemy`
  - `python-dotenv`

Install dependencies using:
```bash
pip install requests sqlalchemy python-dotenv
```

## 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure your code follows the project's style and includes relevant tests.

## 📧 Contact
For questions or feedback, open an issue on GitHub or contact [Helvanljar](https://github.com/Helvanljar).