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
from ShoppingCart import (get_cart_books,add_book_to_cart)
from bookdetails import get_book 
from bookdetails import create_book
from bookdetails import create_author
from Books import get_books, get_books_by_genre, update_book_price_by_publisher, get_books_by_top_seller
from bookdetails import get_book, create_book, create_author, get_authors, get_books_by_author
from Books import get_books, get_books_by_genre, update_book_price_by_publisher

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

# Route to get all books
@app.route('/shopping_cart', methods=['GET'])
def get_cart_book():
    return get_cart_books(mysql)  # Call the function from book_routes.py

# Route to add a book to the shopping cart
@app.route('/shopping_cart', methods=['POST'])
def add_cart_book():
    return add_book_to_cart(mysql)

# Route to POST a book
@app.route('/create-book', methods=['POST'])
def create_book_route():
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

@app.route('/get-book/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    return get_book(mysql, isbn)

# Route to Create/Update Author Profile
@app.route('/create-author', methods=['POST'])
def create_author_route():
    return create_author(mysql)

# Route to GET Authors
@app.route('/authors', methods=['GET'])
def authors_route():
    return get_authors(mysql)

# Route to GET Books by Author
@app.route('/get-books-by-author/<author_id>', methods=['GET'])
def get_books_by_author_route(author_id):
    return get_books_by_author(mysql, author_id)

# Route to GET books by Genre
@app.route('/books_by_genre', methods=['GET'])
def books_by_genre():
    return get_books_by_genre(mysql) 

# Route to PUT a new discount on a book by publisher
@app.route('/books_discount_by_publisher', methods=['PUT'])
def books_discount_by_publisher():
    return update_book_price_by_publisher(mysql) 

# Route to GET books by Top Sellers
@app.route('/books_by_top_seller', methods=['GET'])
def books_by_top_sellers():
    return get_books_by_top_seller(mysql) 

if __name__ == '__main__':
    app.run(debug=True)
