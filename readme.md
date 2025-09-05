# Movies_Project

A Python CLI application to manage your movie collection with database storage, API integration, and website generation.

## Features
- Store movies in an SQLite database
- Fetch movie details (title, year, rating, poster) from the OMDb API
- List, add, delete, update movies
- View statistics and search movies
- Generate a website with your movie collection

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Helvanljar/Movies_Project.git
   cd Movies_Project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OMDb API key:
   ```
   OMDB_API_KEY=your_api_key_here
   ```

## Usage

Run the CLI application:
```bash
python movies.py
```

Menu:
```
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
```

## Website Generation
When choosing option `9. Generate website`, the app creates an `index.html` file (and `style.css` if missing) in the project root.  
Open the file in your browser to view your movie collection.

---

## License
This project is for educational purposes.
