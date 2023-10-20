import mysql.connector
from flask import jsonify,request
import config2
import bcrypt

class AddUser:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=config2.MYSQL_HOST,
            user=config2.MYSQL_USER,
            password=config2.MYSQL_PASSWORD,
            database=config2.MYSQL_DB
        )

    def add_user(self):
        try:
            cursor = self.connection.cursor()
            data=request.json

            password = data.get('password', '')  
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            insert_user_query = "INSERT INTO USER (name, email,isAdmin, password) VALUES (%s, %s, %s, %s)"
            user_values = (data.get('name', ''), data.get('email', ''), data['isAdmin'], hashed_password.decode('utf-8'))
            cursor.execute(insert_user_query, user_values)
            self.connection.commit()
            return jsonify({'message': 'User Added Succesfully '})

        except mysql.connector.Error as db_error:
            print(f"Database Error: {db_error}")
            return jsonify({'message': 'Database Error'})
        except Exception as e:
            self.connection.rollback()
            return jsonify({'message': 'Error'})
        finally:
            cursor.close()


