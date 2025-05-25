DROP TABLE IF EXISTS movie CASCADE;
DROP TABLE IF EXISTS user_profile CASCADE;
DROP TABLE IF EXISTS actors CASCADE;
DROP TABLE IF EXISTS watchlist CASCADE;
DROP TABLE IF EXISTS stars_in CASCADE;
DROP TABLE IF EXISTS rating CASCADE;

CREATE TABLE movie (
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    director TEXT NOT NULL,
    genre TEXT NOT NULL,
    run_time INTEGER NOT NULL,
    movie_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    IMDB_rating REAL NOT NULL,
    num_votes INTEGER NOT NULL,
    poster_url TEXT
);    

CREATE TABLE user_profile (
    password TEXT NOT NULL,
    user_id TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE actors (
    actor_name TEXT NOT NULL,
    actor_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);

CREATE TABLE favourite_actors (
    user_id TEXT NOT NULL,
    actor_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, actor_id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
)

CREATE TABLE watchlist (
    user_id TEXT NOT NULL,
    movie_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

CREATE TABLE stars_in (
    actor_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    PRIMARY KEY (actor_id, movie_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

CREATE TABLE rating (
    user_id TEXT NOT NULL,
    movie_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
);

