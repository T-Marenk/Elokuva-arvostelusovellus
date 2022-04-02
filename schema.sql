CREATE TABLE movies (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE information (id SERIAL PRIMARY KEY, movie_id INTEGER REFERENCES movies, year INTEGER, length INTEGER, genre TEXT);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, movie_id INTEGER REFERENCES movies, stars INTEGER, review TEXT, left_at TIMESTAMP, user_id INTEGER REFERENCES users);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);
CREATE TABLE description (id SERIAL PRIMARY KEY, movie_id INTEGER REFERENCES movies, description TEXT);
