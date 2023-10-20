import mysql.connector
from flask import Flask, request, jsonify
import config2
import json

app = Flask(__name__)
app.config.from_object(config2)

connection = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    autocommit=True
)
cursor = connection.cursor(buffered=True)
with open('imdb.json', 'r') as file:
    movies_data = json.load(file)

try:
    for movie_data in movies_data:
        popularity = movie_data["99popularity"]
        director = movie_data["director"]
        imdb_score = movie_data["imdb_score"]
        name = movie_data["name"]

        

        # Check if the movie already exists
        movie_id_query = "SELECT id FROM movies WHERE name = %s"
        cursor.execute(movie_id_query, (name,))
        existing_movie_id = cursor.fetchone()

        if not existing_movie_id:
            # Insert the movie into the movies table
            insert_movie_query = "INSERT INTO movies (popularity, director, imdb_score, name) VALUES (%s, %s, %s, %s)"
            movie_values = (popularity, director, imdb_score, name)
            cursor.execute(insert_movie_query, movie_values)
            # connection.commit()

            # Retrieve the ID of the inserted movie
            cursor.execute(movie_id_query, (name,))
            movie_id = cursor.fetchone()[0]

            genres_list = movie_data["genre"]

            # Insert genres into the genres table and create relationships
            for genre_name in genres_list:
                insert_genre_query = "INSERT IGNORE INTO genres (name) VALUES (%s)"
                cursor.execute(insert_genre_query, (genre_name,))
                # connection.commit()

                # Retrieve the genre ID
                cursor.execute("SELECT id FROM genres WHERE name = %s", (genre_name,))
                genre_id = cursor.fetchone()[0]

                # Insert relationships into the movie_genres table
                insert_movie_genre_query = "INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)"
                cursor.execute(insert_movie_genre_query, (movie_id, genre_id))

except Exception as e:
    connection.rollback()  # Roll back the transaction in case of an error
    print("Error:", e)
finally:
    cursor.close()
    connection.close()

if __name__ == '__main__':
    app.run()
