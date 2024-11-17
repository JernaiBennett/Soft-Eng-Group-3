from flask import request, jsonify

def get_cart_books(mysql):
    # Get User Id from query parameters
    user_id = request.args.get('UserId')
    print(user_id)
    if not user_id:
        return jsonify({'error': 'User Id is required'}), 400

    try:
        cursor = mysql.connection.cursor()
        # Query to retrieve books in the user's shopping cart
        query = """
            SELECT Book.isbn, Book.name, Book.price, ShoppingCartItem.quantity
            FROM ShoppingCartItem
            JOIN ShoppingCart ON ShoppingCartItem.cart_id = ShoppingCart.id
            JOIN Book ON ShoppingCartItem.book_isbn = Book.isbn
            WHERE ShoppingCart.user_id = %s;
        """
        cursor.execute(query, (int(user_id),))
        books = cursor.fetchall()
        cursor.close()

        print(books)

        # Format the result as a list of book objects
        book_list = []
        for book in books:
            book_obj = {
                'Book Id': book[0],
                'Title': book[1],
                'Price': float(book[2]),
                'Quantity': book[3]
            }
            book_list.append(book_obj)

        return jsonify(book_list), 200

    except Exception as e:
        # Log the exception if needed and return an error response
        return jsonify({'error': str(e)}), 500

def add_book_to_cart(mysql):
    # Get User Id and Book Id from the request data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data in the request body'}), 400

    user_id = data.get('UserId')
    book_id = data.get('BookId')

    if not user_id or not book_id:
        return jsonify({'error': 'User Id and Book Id are required'}), 400

    try:
        cursor = mysql.connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT id FROM User WHERE id = %s", (int(user_id),))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            return jsonify({'error': 'User not found'}), 404

        # Check if the book exists
        cursor.execute("SELECT isbn FROM Book WHERE isbn = %s", (int(book_id),))
        book = cursor.fetchone()
        if not book:
            cursor.close()
            return jsonify({'error': 'Book not found'}), 404

        # Get or create the shopping cart for the user
        cursor.execute("SELECT id FROM ShoppingCart WHERE user_id = %s", (int(user_id),))
        cart = cursor.fetchone()
        if not cart:
            # Create a new shopping cart for the user
            cursor.execute("INSERT INTO ShoppingCart (user_id) VALUES (%s)", (int(user_id),))
            mysql.connection.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart[0]

        # Check if the book is already in the cart
        cursor.execute("""
            SELECT quantity FROM ShoppingCartItem
            WHERE cart_id = %s AND book_isbn = %s
        """, (int(cart_id), int(book_id)))
        item = cursor.fetchone()
        if item:
            # Update the quantity (increment by 1)
            new_quantity = item[0] + 1
            cursor.execute("""
                UPDATE ShoppingCartItem
                SET quantity = %s
                WHERE cart_id = %s AND book_isbn = %s
            """, (new_quantity, int(cart_id), int(book_id)))
        else:
            # Insert the book into the cart with quantity 1
            cursor.execute("""
                INSERT INTO ShoppingCartItem (cart_id, book_isbn, quantity)
                VALUES (%s, %s, %s)
            """, (int(cart_id), int(book_id), 1))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Book added to shopping cart'}), 201

    except Exception as e:
        # Log the exception if needed and return an error response
        return jsonify({'error': str(e)}), 500

def remove_book_from_cart(mysql):
    # Get User Id and Book Id from the request data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data in the request body'}), 400

    user_id = data.get('UserId')
    book_id = data.get('BookId')

    if not user_id or not book_id:
        return jsonify({'error': 'User Id and Book Id are required'}), 400

    try:
        cursor = mysql.connection.cursor()

        # Get the shopping cart for the user
        cursor.execute("SELECT id FROM ShoppingCart WHERE user_id = %s", (int(user_id),))
        cart = cursor.fetchone()
        if not cart:
            cursor.close()
            return jsonify({'error': 'Shopping cart not found for user'}), 404

        cart_id = cart[0]

        # Check if the book is in the cart
        cursor.execute("""
            SELECT quantity FROM ShoppingCartItem
            WHERE cart_id = %s AND book_isbn = %s
        """, (int(cart_id), int(book_id)))
        item = cursor.fetchone()
        if not item:
            cursor.close()
            return jsonify({'error': 'Book not found in shopping cart'}), 404

        quantity = item[0]
        if quantity > 1:
            # Decrease the quantity by 1
            new_quantity = quantity - 1
            cursor.execute("""
                UPDATE ShoppingCartItem
                SET quantity = %s
                WHERE cart_id = %s AND book_isbn = %s
            """, (new_quantity, int(cart_id), int(book_id)))
        else:
            # Remove the book from the cart
            cursor.execute("""
                DELETE FROM ShoppingCartItem
                WHERE cart_id = %s AND book_isbn = %s
            """, (int(cart_id), int(book_id)))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Book removed from shopping cart'}), 200

    except Exception as e:
        # Log the exception if needed and return an error response
        return jsonify({'error': str(e)}), 500

def get_cart_subtotal(mysql):
    # Get User Id from query parameters
    user_id = request.args.get('UserId')
    if not user_id:
        return jsonify({'error': 'User Id is required'}), 400

    try:
        cursor = mysql.connection.cursor()
        # Query to calculate the subtotal price of all items in the user's shopping cart
        query = """
            SELECT SUM(Book.price * ShoppingCartItem.quantity) as subtotal
            FROM ShoppingCartItem
            JOIN ShoppingCart ON ShoppingCartItem.cart_id = ShoppingCart.id
            JOIN Book ON ShoppingCartItem.book_isbn = Book.isbn
            WHERE ShoppingCart.user_id = %s;
        """
        cursor.execute(query, (int(user_id),))
        result = cursor.fetchone()
        cursor.close()

        # If the cart is empty, subtotal will be None
        subtotal = result[0] if result[0] is not None else 0.0

        # Return the subtotal as JSON
        return jsonify({'Subtotal': float(subtotal)}), 200

    except Exception as e:
        # Log the exception if needed and return an error response
        return jsonify({'error': str(e)}), 500