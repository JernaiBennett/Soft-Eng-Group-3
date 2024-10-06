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
                'Price': book[2],
                'Quantity': book[3]
            }
            book_list.append(book_obj)

        return jsonify(book_list), 200

    except Exception as e:
        # Log the exception if needed and return an error response
        return jsonify({'error': str(e)}), 500
