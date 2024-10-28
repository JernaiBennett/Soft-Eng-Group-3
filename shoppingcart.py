from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection parameters
db_config = {
    'host': 'localhost',     # Replace with your MySQL host
    'user': 'root',          # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'database': 'shopping_db'  # Replace with your MySQL database name
}

# Create a connection to the MySQL database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Route to retrieve the subtotal price of all items in the user's shopping cart
@app.route('/cart/subtotal/<user_id>', methods=['GET'])
def get_cart_subtotal(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT SUM(price * quantity) AS subtotal FROM cart WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    subtotal = result['subtotal'] if result['subtotal'] is not None else 0

    cursor.close()
    connection.close()

    return jsonify({'subtotal': subtotal})

# Route to add a book to the shopping cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('userId')
    book_id = data.get('bookId')
    price = data.get('price')
    quantity = data.get('quantity')

    if not user_id or not book_id or not price or not quantity:
        return jsonify({'message': 'Invalid request data'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    # Insert the new book into the cart or update the quantity if it already exists
    cursor.execute("""
        INSERT INTO cart (user_id, book_id, price, quantity)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
    """, (user_id, book_id, price, quantity))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Book added to cart'})

# Route to retrieve the list of book(s) in the user's shopping cart
@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT book_id, price, quantity FROM cart WHERE user_id = %s", (user_id,))
    cart_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(cart_items)

# Route to delete a book from the shopping cart
@app.route('/cart/delete', methods=['DELETE'])
def delete_from_cart():
    data = request.json
    user_id = data.get('userId')
    book_id = data.get('bookId')

    if not user_id or not book_id:
        return jsonify({'message': 'Invalid request data'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM cart WHERE user_id = %s AND book_id = %s", (user_id, book_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Book removed from cart'})

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
