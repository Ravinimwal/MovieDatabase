# MovieDatabase


## Table of Contents
1. [Configuration Setup](#configuration-setup)
2. [Testing Add User API](#testing-add-user-api)
3. [Testing Search Movies API](#testing-search-movies-api)
4. [Testing Add Movies API](#testing-add-movies-api)
5. [Testing Get All Movies API](#testing-get-all-movies-api)
6. [Testing Update Movies API](#testing-update-movies-api)
7. [Testing Delete Movies API](#testing-delete-movies-api)


### Configuration Setup
1) Open Command Prompt and  enter the following command - https://github.com/Ravinimwal/MovieDatabase.git
2) Open the MovieDatabase.sql in workbench and execute all the commands to create tables
3) Now browse to the newly created folder using the command - cd MovieDatabse
4) Run the following command to create a new conda virtual environment in current folder- conda create -p ./venv python=3.8 -y
5) Enter Command - conda activate venv/
6) Run the command - {pip install -r requirements.txt} to install the required libraries
7) In the config2.py file, set up your MySQL database configuration:
8) Enter Command -> python addListFromJson.py , this will add the movies in the imdb.json file to the database
9) Enter Command -> python userFunctions.py
10) Note Down the server and open postman and paste it in url box (below image is for reference)
![image](https://github.com/Mayankrai01/MovieDatabase/assets/103130321/4099fe2c-8708-488e-8bd0-062bb532bcd5)



### Testing Add User API
1) Edit the URL to - http://127.0.0.1:5000/adduser
2) Set Request to POST METHOD
3) Add the data given below in body->raw->json
4) {
    "name":"testuser",
    "email":"testuser@g.com",
    "isAdmin":false,
    "password":"passwordtest2"
  }
5) {
    "name":"testadmin",
    "email":"admin@g.com",
    "isAdmin":true,
    "password":"adminpass"
  }
6) Run the following command in your MYSQL workbench to check if the users are added- {select * from user;}
7) It would show the two users with their names


### Testing Search Movies API
1) Edit the URL to -http://127.0.0.1:5000/searchmovies
2) Method- GET
3) Add the data given below in body->raw->json
4) A general format to search based of different criterions is given below-
5) To search using genres-
  {
      "genre":["Adventure"]
  }
6) To search using name-
  {
      "movie_name":"Star Wars"
  }
7) To search using director -
  {
      "director":"Victor Fleming"
  }


### Testing Add Movies API
1) Edit the URL to -http://127.0.0.1:5000/movies
2) Method - POST
3) Add the data given below in body->raw->json
4) {
    "name":"Big Bang Theory",
    "user_email":"admin@g.com",
    "entered_password":"adminpass",
    "popularity":"92",
    "director":"Chuck Lore",
    "imdb_score":8.8,
    "genre":["Romcom","Drama"]
  }
5) Movie should be successfully added to database check using the command -{SELECT * from movies;} and browse to the last inserted value


### Testing Get All Movies API
1) Edit the URL to -http://127.0.0.1:5000/movies
2) Method - GET
3) Send the request and you should get all the movies list


### Testing Update Movies API
1) Edit the URL to -http://127.0.0.1:5000/movies
2) Method - PUT
3) Add the data given below in body->raw->json
4) {
    "name":"Big Bang Theory",
    "user_email":"admin@g.com",
    "entered_password":"adminpass",
    "popularity":"92",
    "imdb_score":8.8,
    "director":"Chuck Lore",
    "new_name":"The Big Bang Theory",
    "new_popularity":"92",
    "new_imdb_score":8.8,
    "new_director":"Chuck Lore"
  }
5) See the updated movies table and the name of the "Big Bang Theory" movie would be update to "The Big Bang Theory"

### Testing Delete Movies API
1) Edit the URL to -http://127.0.0.1:5000/movies
2) Method - DELETE
3) Add the data given below in body->raw->json
4) {
    "name":"The Big Bang Theory",
    "user_email":"admin@g.com",
    "entered_password":"adminpass",
    "popularity":"92",
    "imdb_score":8.8,
    "director":"Chuck Lore"
  }
5) See the updated movies table and the movie "Big Bang Theory" would be deleted
