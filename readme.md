# Movie App 🎬

A command-line movie manager with OMDb API integration and static
website generator.

## Features

-   Add movies by title (details fetched automatically from OMDb API)
-   List all movies
-   Delete movies
-   Update movies manually (optional)
-   View statistics (average, median, best/worst rated)
-   Pick a random movie
-   Search movies
-   Sort movies by rating
-   Generate a static website with your movie collection

## Installation

1.  Clone the repository:

    ``` bash
    git clone https://github.com/YOUR_USERNAME/movie-app.git
    cd movie-app
    ```

2.  Create a virtual environment and activate it:

    ``` bash
    python -m venv .venv
    source .venv/bin/activate   # macOS/Linux
    .venv\Scripts\activate    # Windows
    ```

3.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Create a `.env` file in the project root and add your OMDb API key:

        OMDB_API_KEY=your_api_key_here

## Usage

Run the CLI app:

``` bash
python movies.py
```

Menu options:

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

The generated website (`index.html` + `style.css`) will appear in the
`_static` folder.

## Notes

-   Make sure to **never commit your `.env` file**. Your API key should
    remain private.
-   Use `.env.example` to share a template with collaborators.

## License

MIT License
