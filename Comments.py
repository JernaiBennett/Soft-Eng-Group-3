from flask import jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

def get_comments(mysql, book_isbn):
    # Retrieve book ISBN from request parameters
    print(f"Fetching comments for book ISBN: {book_isbn}")

    cur = mysql.connection.cursor()
    query = "SELECT * FROM Comment WHERE book_isbn = %s"
    cur.execute(query, (book_isbn,))
    rows = cur.fetchall()
    cur.close()

    if not rows:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(rows)

def add_comment(mysql):
    # Retrieve data from the request body
    data = request.get_json()
    book_isbn = data.get('book_isbn')
    user_id = data.get('user_id')
    comment = data.get('comment')
    date_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time

    # Validate required fields
    if not (book_isbn and user_id and comment):
        return jsonify({"error": "Missing fields"}), 400

    cur = mysql.connection.cursor()
    try:
        # Insert the comment (this will fail if the book does not exist)
        query = "INSERT INTO Comment (book_isbn, user_id, comment, date_stamp) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (book_isbn, user_id, comment, date_stamp))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Comment added successfully", "date_stamp": date_stamp}), 201

    except Exception as e:
        # Check if the error message includes 'book_isbn' to identify the foreign key violation on `book_isbn`
        if 'book_isbn' in str(e):
            return jsonify({"error": "Book not found"}), 404
        else:
            # General database error handling for other Error cases
            return jsonify({"error": "Database error occurred"}), 500
    finally:
        cur.close()
