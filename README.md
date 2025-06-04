# IMDB-Copy

A Flask-based web application that replicates core IMDB functionality with a PostgreSQL database backend.

## Table of Contents:
1. [Background information](#background-information)
2. [Prerequisites](#prerequisites)
3. [Clone the GitHub Repository](#clone-the-github-repository)
4. [Setup with Docker](#setup-with-docker)
5. [Setup without Docker](#setup-without-docker)
6. [Accessing the application](#accessing-the-application)
7. [E/R Diagram](#er-diagram)

## Background information
Our app uses python and flask for the backend, postgresql to interact with the database, and javascript and ReactJS for the 
frontend. 

Our database is from the following [kaggle database](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows).

## Prerequisites
- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)
- npm (node package manager)
- Docker Desktop + Docker VS Code extension (optional)

## Clone the GitHub repository
```
git clone https://github.com/sabetsain/IMDB-Copy.git
cd IMDB-Copy
```

## Setup with Docker
If you have both docker desktop installed, as well as the IDE extension, then you can run the following
from the root directory:
```
docker compose up
```
in the terminal, and the application will run.

If running in docker container, then check the following lines of code in the respective files:
* flaskr/db.py 
```
(...)
11    # pg_uri = "postgresql://dis_project:dis_project@localhost:5432/imdb_copy"
12    pg_uri = "postgresql://dis_project:dis_project@db:5432/imdb_copy"
(...)
```
* frontend/src/api.js:
```
1     // const API_URL = "http://127.0.0.1:5000/api";
2     const API_URL = "http://127.0.0.1:5001/api";
(...)
```
**NOTE**: Each time you compose the docker container, any information held in the databases will be cleaned, so
for example, you will have to register a new log in.

## Setup without Docker
1. Install required dependencies:
   ```
   pip install -r flaskr/requirements.txt
   cd frontend
   npm install
   cd ..
   ```

2. Set up the PostgreSQL database:
   - Create a database named "imdb_copy"
   - Create a user named "dis_project" with password "dis_project"
   - Grant this user all privileges on the "imdb_copy" database

3. Initialize the application:
   ```
   flask init-db
   ```
   You should see the message "Initialized the database."

4. Again, check the following lines in the respective lines of code:
* flaskr/db.py 
```
(...)
11    pg_uri = "postgresql://dis_project:dis_project@localhost:5432/imdb_copy"
12    # pg_uri = "postgresql://dis_project:dis_project@db:5432/imdb_copy"
(...)
```
* frontend/src/api.js:
```
1     const API_URL = "http://127.0.0.1:5000/api";
2     // const API_URL = "http://127.0.0.1:5001/api";
(...)
```

5. To start the development server:
* Backend (from the root directory):
```
flask --app flaskr run --debug
```
* Frontend:
```
cd frontend
npm run dev
```

## Accessing the application
Visit http://localhost:5173/ in your browser to view the application.

1. To begin, register a new account. Ensure that your username only uses valid characters (lower and uppercase characters,
numbers, dashes, periods, and underscores). Any other character types won't be accepted in your username.
2. Once you have registered, head over to the login page and login using the account you just set up.
3. Now you are able to rate movies, add movies to your watchlist, and browse/choose favorite actors. To rate a movie,
simply click on the the stars found under a given movie. As well, to add a movie to your watchlist, simply click the button
labeled 'Add to Watchlist'.
4. To see which movies you have rated or added to your watchlist, just click on your username in the top right corner, and 
you will find a dropdown menu where you can navigate to those respective pages.
5. Lastly, on any given page, you can navigate using the search bar. Start searching for your favorite movie to try it out!

## E/R Diagram
In the below E/R diagram, we present the relationships between the tables in our database. Most notable is maybe that all 
relations between tables have a many-to-many relationship. We elaborate in our three cases:

1. **Movies ratings**: Multiple users are able to give the same movie different ratings, and one user is able to give ratings 
to multiple different movies.
2. **Favorite Actors**: An actor is able to be favorited by multiple users, but one user can also favorite multiple actors.
3. **Watchlist**: One movie can exist in the watchlist of multiple users, but one user can also have multiple movies in 
their watchlist.

![E/R Diagram](./data/E:R%20Diagram%20DIS%20Project.png)