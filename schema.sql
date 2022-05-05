CREATE TABLE movies (
	id SERIAL PRIMARY KEY,
       	name TEXT,
	year INTEGER,
	length INTEGER,
	genre TEXT	
);

CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
       	movie_id INTEGER REFERENCES movies,
       	stars INTEGER,
       	review TEXT,
       	left_at TIMESTAMP,
       	user_id INTEGER
       	REFERENCES users
);

CREATE TABLE users (id SERIAL PRIMARY KEY,
       	username TEXT,
       	password TEXT,
       	admin BOOLEAN
);

CREATE TABLE description (
	id SERIAL PRIMARY KEY,
       	movie_id INTEGER REFERENCES movies,
       	description TEXT
);

CREATE TABLE pending (
	id SERIAL PRIMARY KEY,
	movie_name TEXT,
	year INTEGER
);

CREATE TABLE platforms (
	id SERIAL PRUMARY KEY,	
	name TEXT,
	link TEXT
);

CREATE TABLE view_at (
	movie_id INTEGER,
       	patform_id INTEGER
);
