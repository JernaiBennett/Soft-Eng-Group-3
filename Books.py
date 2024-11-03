from flask import jsonify, request

######################## Get All Books ########################
def get_books(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Book")
    rows = cur.fetchall()

    books = []
    for row in rows:
        book = {
            'isbn': row[0],
            'name': row[1],
            'description': row[2],
            'price': row[3],
            'author_id': row[4],
            'genre': row[5],
            'publisher_id': row[6],
            'year_published': row[7],
            'copies_sold': row[8]
        }
        books.append(book)

    cur.close()
    
    return jsonify(books)

######################## Get All Books w/ Genre ########################
def get_books_by_genre(mysql):
    genre = request.args.get('genre')

    if not genre:
        return jsonify({'error': 'Genre is required'}), 400

    try:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM Book WHERE genre = %s"
        cur.execute(query, (genre,))
        rows = cur.fetchall()

        if not rows:
            return jsonify({'message': f'No books found for genre: {genre}'}), 404

        books = []
        for row in rows:
            book = {
                'isbn': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'author_id': row[4],
                'genre': row[5],
                'publisher_id': row[6],
                'year_published': row[7],
                'copies_sold': row[8]
            }
            books.append(book)
        
        return jsonify({'message': 'Books received successfully', 'data': books}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred during the get process'}), 500

    finally:
        cur.close()

######################## Update All Books w/ New Price by Discount and Publisher ########################
def update_book_price_by_publisher(mysql):
    discount = request.args.get('discount')
    publisher = request.args.get('publisher')

    try:
        discount = float(discount) / 100
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid discount value'}), 400

    if (not publisher):
        return jsonify({'error': 'Publisher not provided'}), 400

    try:
        cur = mysql.connection.cursor()

        get = """SELECT bookstore.Book.name as book_name, bookstore.Publisher.name as publisher, price FROM bookstore.Book
                INNER JOIN bookstore.Publisher
                ON publisher_id = bookstore.Publisher.id
                WHERE bookstore.Publisher.name = %s"""
        cur.execute(get, (publisher,))

        books = []
        rows = cur.fetchall()

        if not rows:
            return jsonify({'error': 'No books found for the given publisher'}), 404
        
        for row in rows:
            old_price = float(row[2]) 
            new_price = round(old_price * (1 - discount), 2) 
            book = {
                "name": row[0],
                "publisher": row[1],
                "old_price": old_price,
                "new_price": new_price
            }

            books.append(book)
    
        update = """UPDATE bookstore.Book 
                INNER JOIN bookstore.Publisher
                ON publisher_id = bookstore.Publisher.id
                SET price = ROUND(price * %s, 2)
                WHERE bookstore.Publisher.name = %s"""

        cur.execute(update, (1 - discount, publisher,))
        mysql.connection.commit()

        return jsonify({'message': 'Book prices updated successfully', 'data': books}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred during the update process'}), 500
    
    finally:
        cur.close()

######################## Get All Books By Top Seller (W/ Limit) ########################
def get_books_by_top_seller(mysql):
    try:
        cur = mysql.connection.cursor()
        query = """SELECT * FROM bookstore.Book
                    ORDER BY copies_sold DESC
                    LIMIT 10;"""
        cur.execute(query,)
        rows = cur.fetchall()

        if not rows:
            return jsonify({'message': f'No books found.'}), 404

        books = []
        for row in rows:
            book = {
                'isbn': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'author_id': row[4],
                'genre': row[5],
                'publisher_id': row[6],
                'year_published': row[7],
                'copies_sold': row[8]
            }
            books.append(book)
        
        return jsonify({'message': 'Books received   successfully', 'data': books}), 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred during the get process'}), 500

    finally:
        cur.close()