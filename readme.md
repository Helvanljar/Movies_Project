# Movies_Project 🎨

A Python CLI application to manage movies with user profiles, notes, posters, ratings, and website generation.

## Features

- Multiple user profiles
- Add movies from OMDb API
- Store movie title, year, rating, poster URL, notes, and country
- Delete movies
- Update movie notes
- List movies with ratings, notes, and country flags
- Statistics: average, median, best/worst movies
- Search movies
- Random movie selection
- Sort movies by rating
- Generate HTML website for each user's movie collection

## Installation

1. Clone the repository:

```bash
git clone <YOUR_REPO_URL>
cd Movies_Project
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

- Windows:

```bash
.venv\Scripts\activate
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your OMDb API key:

```env
OMDB_API_KEY=your_api_key_here
```

## Usage

1. Run the CLI:

```bash
python movies.py
```

2. Select or create a user profile.
3. Use the menu to add, delete, update, or list movies.
4. Generate the website (option 9) to create an HTML view of your movie collection.
5. Exit the application with option 0.

## Project Structure

```
Movies_Project/
├── movies.py               # CLI main file
├── movie_storage_sql.py    # SQL storage with SQLAlchemy
├── generate_website.py     # Website generator
├── _static/                # CSS and HTML output
├── .env                    # OMDb API key
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── ...
```

## Notes

- Ensure the `.env` file is never committed to public repositories.
- The generated website will be stored in the `_static/` directory.
- Ratings, notes, and country flags are displayed on the website.
- Each user has a separate movie collection.

