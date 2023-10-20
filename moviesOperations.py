# models.py
from flask import Flask, request, jsonify
import mysql.connector
import json
import config2
import bcrypt

class MovieModel:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=config2.MYSQL_HOST,
            user=config2.MYSQL_USER,
            password=config2.MYSQL_PASSWORD,
            database=config2.MYSQL_DB
        )
        
    def get_movies(self):
        cursor = self.connection.cursor(buffered=True)
        cursor.execute('SELECT id, name, director, imdb_score, popularity FROM movies')

        movies = cursor.fetchall()
        cursor.close()
        return jsonify(movies)
    
    def add_movie(self):
        movie_data=request.json
        cursor = self.connection.cursor()
        query = "SELECT * FROM USER WHERE email = %s"
        cursor.execute(query, (movie_data['user_email'],))
        result = cursor.fetchall()
        if(len(result)==0):
            return jsonify({'message': 'No user with such credentials exits'}), 201
        else:
            password = result[0][3]
            if not bcrypt.checkpw(movie_data['entered_password'].encode('utf-8'), password.encode('utf-8')):
                return jsonify({'message': 'Incorrect Credentials'}), 201
            if bcrypt.checkpw(movie_data['entered_password'].encode('utf-8'), password.encode('utf-8')):
                if(result[0][2]==False):
                    return jsonify({'message': 'No Access'}), 201
                else:
                    popularity = movie_data["popularity"]
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
                            self.connection.commit()
                        return jsonify({'message': 'Movie Added successfully'}), 201
                    return jsonify({'message': 'Movie Already exits'})
            
    def delete_movie(self):
        movie_data = request.json
        # Check if the movie already exists
        cursor = self.connection.cursor()
        query = "SELECT * FROM USER WHERE email = %s"
        cursor.execute(query, (movie_data['user_email'],))
        result = cursor.fetchall()
        if(len(result)==0):
            return jsonify({'message': 'No user with such credentials exits'}), 201
        else:
            password = result[0][3]
            if not bcrypt.checkpw(movie_data['entered_password'].encode('utf-8'), password.encode('utf-8')):
                return jsonify({'message': 'Incorrect Credentials'}), 201
            if bcrypt.checkpw(movie_data['entered_password'].encode('utf-8'), password.encode('utf-8')):
                if(result[0][2]==False):
                    return jsonify({'message': 'No Access'}), 201
                else:
                    movie_id_query = "SELECT id FROM movies WHERE name = %s AND director = %s AND imdb_score = %s AND popularity = %s"
                    cursor.execute(movie_id_query, (movie_data['name'], movie_data['director'], movie_data['imdb_score'], movie_data['popularity']))
                    existing_movie_id = cursor.fetchone()

                    if existing_movie_id:

                        query = "DELETE FROM movie_genres WHERE movie_id = %s;"
                        cursor.execute(query, existing_movie_id)           

                        
                        query = "DELETE FROM movies WHERE id =%s;"
                        cursor.execute(query, existing_movie_id)
                        self.connection.commit()

                        return jsonify({'message': 'Movie Deleted successfully'}), 201
                    
                    else:
                        return jsonify({'message': 'Movie does not exist'}), 404
                    
    def update_movie(self):
        movie_data = request.json

        # Check if the movie already exists
        cursor = self.connection.cursor()
        movie_data = request.json
        # Check if the movie already exists
        cursor = self.connection.cursor()
        query = "SELECT * FROM USER WHERE email = %s"
        cursor.execute(query, (movie_data['user_email'],))
        result = cursor.fetchall()
        if(len(result)==0):
            return jsonify({'message': 'No user with such credentials exits'}), 201
        else:
            password = result[0][3]
            if not bcrypt.checkpw(movie_data['entered_password'].encode('utf-8'), password.encode('utf-8')):
                return jsonify({'message': 'Incorrect Credentials'}), 201
            if bcrypt.checkpw(movie_data['entered_password'].encode('utf-8'), password.encode('utf-8')):
                if(result[0][2]==False):
                    return jsonify({'message': 'No Access'}), 201
                else:            
                    movie_id_query = "SELECT id FROM movies WHERE name = %s AND director = %s AND imdb_score = %s AND popularity = %s"
                    cursor.execute(movie_id_query, (movie_data['name'], movie_data['director'], movie_data['imdb_score'], movie_data['popularity']))
                    existing_movie_id = cursor.fetchone()

                    if existing_movie_id:

                        query = "UPDATE movies SET name = %s, director = %s, imdb_score = %s, popularity = %s WHERE id = %s"
                        new_details = (
                            movie_data.get('new_name'),
                            movie_data.get('new_director'),
                            movie_data.get('new_imdb_score'),
                            movie_data.get('new_popularity'),
                            existing_movie_id[0]  
                        )
                        cursor.execute(query, new_details)
                        self.connection.commit()

                        return jsonify({'message': 'Movie Updated successfully'}), 201
                    
                    else:
                        return jsonify({'message': 'Movie does not exist'}), 404

