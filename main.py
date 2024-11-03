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
from Comments import add_comment, get_comments
from BookRating import get_average_rating

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
def bookdetails_route1(isbn):
    return get_book(mysql, isbn)

# Route to GET comments for a specific book by ISBN
@app.route('/comments', methods=['GET'])
def get_comments_for_book(book_isbn):
    return get_comments(mysql, book_isbn)

# Route to POST a comment with a datestamp
@app.route('/create_comment', methods=['POST'])
def add_comment_route():
    return add_comment(mysql)

# Route to GET the average rating
@app.route('/average_rating', methods=['GET'])
def average_rating_route():
    return get_average_rating(mysql)


if __name__ == '__main__':
    app.run(debug=True)
