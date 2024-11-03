# to run, type python main.py in terminal

# flask is the server
from flask import Flask, request, jsonify
# provides MySQL connection for Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from Books import get_books 
from ShoppingCart import (get_cart_books,add_book_to_cart, remove_book_from_cart)

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

# Route to delete a book from the shopping cart
@app.route('/shopping_cart', methods=['DELETE'])
def delete_from_shopping_cart_route():
    return remove_book_from_cart(mysql)

if __name__ == '__main__':
    app.run(debug=True)
