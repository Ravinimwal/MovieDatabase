import mysql.connector
import config2  
from flask import Flask, request, jsonify


class getSearchResults:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=config2.MYSQL_HOST,
            user=config2.MYSQL_USER,
            password=config2.MYSQL_PASSWORD,
            database=config2.MYSQL_DB
        )
    
    def getMovie(self):
        data=request.json
        # Query to retrieve movie details along with movie name
        if('movie_name' in data):
            cursor = self.connection.cursor(buffered=True,dictionary=True)

            query = """
                SELECT m.*, GROUP_CONCAT(g.name) AS genres
                FROM movies m
                JOIN movie_genres mg ON m.id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.id
                WHERE m.name = %s
                GROUP BY m.id
            """
            cursor.execute(query, (data['movie_name'],))
            movie_details = cursor.fetchall()

            cursor.close()
            
            return jsonify(movie_details)

        # Query to retrieve movie details along with genre names
        elif('genre' in data):
            movie_details =[]
            cursor = self.connection.cursor(buffered=True,dictionary=True)
            for genre in data['genre']:
                query = """
                    SELECT m.*, GROUP_CONCAT(g.name) AS genres
                    FROM movies m
                    JOIN movie_genres mg ON m.id = mg.movie_id
                    JOIN genres g ON mg.genre_id = g.id
                    WHERE g.name = %s
                    GROUP BY m.id
                """
                cursor.execute(query, (genre,))
                movie_details_temp= cursor.fetchall()
                movie_details.append(movie_details_temp)
                

            cursor.close()
            # self.connection.close()
            return jsonify(movie_details)
        
        # Query to retrieve movie details along with director names
        elif('director' in data):
            cursor = self.connection.cursor(buffered=True,dictionary=True)

            query = """
                SELECT m.*, GROUP_CONCAT(g.name) AS genres
                FROM movies m
                JOIN movie_genres mg ON m.id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.id
                WHERE m.director = %s
                GROUP BY m.id
            """
            cursor.execute(query, (data['director'],))
            movie_details = cursor.fetchall()

            cursor.close()
            # self.connection.close()
            return jsonify(movie_details)
        
        # Query to retrieve movie details along with imdb rating greater than a value
        elif('imdb_rating' in data):
            cursor = self.connection.cursor(buffered=True,dictionary=True)

            query = """
                SELECT m.*, GROUP_CONCAT(g.name) AS genres
                FROM movies m
                JOIN movie_genres mg ON m.id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.id
                WHERE m.imdb_score >= %s
                GROUP BY m.id
            """
            cursor.execute(query, (data['imdb_rating'],))
            movie_details = cursor.fetchall()

            cursor.close()
            # self.connection.close()            
            return jsonify(movie_details)
        
        else:
            return jsonify({'message': 'Enter Valid Input for Searching Movies'})