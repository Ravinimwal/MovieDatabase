from flask import Flask, request, jsonify
import mysql.connector
import config2
from searchMoviesResult import getSearchResults
from moviesOperations import MovieModel
from addUser import AddUser
AddUser=AddUser()
movieCRUD = MovieModel()
searchMovie=getSearchResults()
app = Flask(__name__)
app.config.from_object(config2)

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)


@app.route('/adduser', methods=['POST'])
def addUser():
    if request.method == 'POST':
        return AddUser.add_user()

@app.route('/movies', methods=['GET', 'POST','DELETE','PUT'])
def movies():
    if request.method == 'GET':
        return movieCRUD.get_movies()
    elif request.method == 'POST':
        return movieCRUD.add_movie()
            
    elif request.method == 'DELETE':
        return movieCRUD.delete_movie()

    elif request.method == 'PUT':
        return movieCRUD.update_movie()


@app.route('/searchmovies', methods=['GET'])
def search():
    return searchMovie.getMovie()

if __name__=='__main__':
    app.run()