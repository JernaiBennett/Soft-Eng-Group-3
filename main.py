# to run, type python main.py in terminal

# flask is the server
from flask import Flask, request, jsonify
# provides MySQL connection for Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from Books import get_books 
from bookdetails import get_book 
from bookdetails import create_book

print("API is running")

app = Flask(__name__)

# Load the .env file
load_dotenv()

# Set MySQL configurations using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Route to get all books
@app.route('/books', methods=['GET'])
def books_route():
    return get_books(mysql)  # Call the function from book_routes.py

# Route to POST a book
@app.route('/bookdetails', methods=['POST'])
def bookdetails_route():
    return create_book(mysql)

# Route to GET a book using ISBN
@app.route('/bookdetails/<isbn>', methods=['GET'])
def bookdetails_route(isbn):
    return get_book(mysql, isbn)

if __name__ == '__main__':
    app.run(debug=True)
