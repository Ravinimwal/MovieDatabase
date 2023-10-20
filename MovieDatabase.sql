CREATE DATABASE DB_MOVIES;
USE DB_MOVIES;

CREATE TABLE movies(
	id INT AUTO_INCREMENT PRIMARY KEY,
    popularity DECIMAL(5,2) NOT NULL,
    director VARCHAR(255) NOT NULL,
    imdb_score DECIMAL(3,1) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE table genres(
	id INT auto_increment PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE table movie_genres(
	movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id,genre_id),
    foreign key (movie_id) references movies(id),
    foreign key (genre_id) references genres(id)
);
CREATE TABLE USER(
	name varchar(255),
    email varchar(255) UNIQUE PRIMARY KEY,
    isAdmin bool default False,
    password varchar(255)
);





select * from user;            
SELECT * from movies;
SELECT * from genres;
select * from movie_genres;
