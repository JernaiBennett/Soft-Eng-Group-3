# Standard library imports
from http import HTTPStatus
from decimal import Decimal

# Flask and extensions
from flask import Flask, request, jsonify
from flask_cors import CORS

# MySQL connector
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Database connection configuration
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="bookstore.cvg0myqa4kzu.us-east-1.rds.amazonaws.com",
            user="admin",
            password="PMw2OzYPsVab0wu6w3t9",
            database="bookstore",
            auth_plugin="mysql_native_password"
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Routes
@app.route('/wishlist', methods=['POST'])
def create_wishlist():
    """Create a new wishlist for a user"""
    try:
        data = request.get_json()
        if not all(k in data for k in ['user_id', 'name']):
            return jsonify({'error': 'Missing required fields'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        cursor.execute("SELECT id FROM User WHERE id = %s", (data['user_id'],))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND

        # Check if wishlist name already exists for this user
        cursor.execute(
            "SELECT id FROM Wishlist WHERE user_id = %s AND name = %s", 
            (data['user_id'], data['name'])
        )
        if cursor.fetchone():
            return jsonify({'error': 'Wishlist name already exists'}), HTTPStatus.CONFLICT

        # Create new wishlist
        cursor.execute(
            "INSERT INTO Wishlist (name, user_id) VALUES (%s, %s)",
            (data['name'], data['user_id'])
        )
        conn.commit()

        return '', HTTPStatus.CREATED

    except Error as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@app.route('/wishlist/book', methods=['POST'])
def add_book_to_wishlist():
    """Add a book to a wishlist"""
    try:
        data = request.get_json()
        if not all(k in data for k in ['book_isbn', 'wishlist_id']):
            return jsonify({'error': 'Missing required fields'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if book and wishlist exist
        cursor.execute("SELECT isbn FROM Book WHERE isbn = %s", (data['book_isbn'],))
        if not cursor.fetchone():
            return jsonify({'error': 'Book not found'}), HTTPStatus.NOT_FOUND

        cursor.execute("SELECT id FROM Wishlist WHERE id = %s", (data['wishlist_id'],))
        if not cursor.fetchone():
            return jsonify({'error': 'Wishlist not found'}), HTTPStatus.NOT_FOUND

        # Check if book already in wishlist
        cursor.execute(
            """SELECT id FROM WishlistItem 
            WHERE wishlist_id = %s AND book_isbn = %s""",
            (data['wishlist_id'], data['book_isbn'])
        )
        if cursor.fetchone():
            return jsonify({'error': 'Book already in wishlist'}), HTTPStatus.CONFLICT

        # Add book to wishlist
        cursor.execute(
            """INSERT INTO WishlistItem (wishlist_id, book_isbn) 
            VALUES (%s, %s)""",
            (data['wishlist_id'], data['book_isbn'])
        )
        conn.commit()

        return '', HTTPStatus.CREATED

    except Error as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@app.route('/wishlist/book', methods=['DELETE'])
def remove_book_from_wishlist():
    """Remove a book from wishlist and optionally add to cart"""
    try:
        data = request.get_json()
        if not all(k in data for k in ['book_isbn', 'wishlist_id']):
            return jsonify({'error': 'Missing required fields'}), HTTPStatus.BAD_REQUEST

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get wishlist item and user
        cursor.execute(
            """SELECT w.user_id, wi.id 
            FROM WishlistItem wi 
            JOIN Wishlist w ON wi.wishlist_id = w.id 
            WHERE wi.wishlist_id = %s AND wi.book_isbn = %s""",
            (data['wishlist_id'], data['book_isbn'])
        )
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Book not found in wishlist'}), HTTPStatus.NOT_FOUND

        # Begin transaction
        conn.start_transaction()

        # Get or create shopping cart
        cursor.execute(
            "SELECT id FROM ShoppingCart WHERE user_id = %s",
            (result['user_id'],)
        )
        cart = cursor.fetchone()
        if not cart:
            cursor.execute(
                "INSERT INTO ShoppingCart (user_id) VALUES (%s)",
                (result['user_id'],)
            )
            cart_id = cursor.lastrowid
        else:
            cart_id = cart['id']

        # Add to cart
        cursor.execute(
            """INSERT INTO ShoppingCartItem (cart_id, book_isbn, quantity) 
            VALUES (%s, %s, 1)""",
            (cart_id, data['book_isbn'])
        )

        # Remove from wishlist
        cursor.execute(
            "DELETE FROM WishlistItem WHERE id = %s",
            (result['id'],)
        )

        conn.commit()
        return '', HTTPStatus.NO_CONTENT

    except Error as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@app.route('/wishlist/<int:wishlist_id>/books', methods=['GET'])
def get_wishlist_books(wishlist_id):
    """Get all books in a wishlist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if wishlist exists
        cursor.execute("SELECT id FROM Wishlist WHERE id = %s", (wishlist_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Wishlist not found'}), HTTPStatus.NOT_FOUND

        # Get books in wishlist
        cursor.execute(
            """SELECT b.isbn, b.name, b.description, b.price, b.genre
            FROM Book b
            JOIN WishlistItem wi ON wi.book_isbn = b.isbn
            WHERE wi.wishlist_id = %s""",
            (wishlist_id,)
        )
        books = cursor.fetchall()

        # Convert Decimal objects to float for JSON serialization
        for book in books:
            if book['price']:
                book['price'] = float(book['price'])

        return jsonify(books), HTTPStatus.OK

    except Error as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
