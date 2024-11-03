from flask import jsonify, request
# from flask_mysqldb import MySQL

# # Initialize the Flask app
# app = Flask(__name__)

# # Configure MySQL connection
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'your_username'
# app.config['MYSQL_PASSWORD'] = 'your_password'
# app.config['MYSQL_DB'] = 'your_database'

# mysql = MySQL(app)

def get_average_rating(mysql):
    book_isbn = request.args.get('book_isbn')

    if not book_isbn:
        return jsonify({"error": "Book ISBN is required"}), 400

    try:
        cur = mysql.connection.cursor()
        # Use the SQL query shared by your classmate
        query = """
            SELECT Book.name AS book_name, 
                   ROUND(AVG(Rating.rating), 2) AS avg_rating 
            FROM bookstore.Rating
            INNER JOIN bookstore.Book ON Rating.book_isbn = Book.isbn
            WHERE Book.isbn = %s
            GROUP BY Book.name
        """
        cur.execute(query, (book_isbn,))
        result = cur.fetchone()

        if not result:
            return jsonify({"error": "No ratings found for this book ISBN"}), 404

        book_name, avg_rating = result

        return jsonify({
            "book_isbn": book_isbn,
            "book_name": book_name,
            "average_rating": avg_rating
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()

# All flask set ups are managed by main.py
# @app.route('/average_rating', methods=['GET'])
# def average_rating_route():
#     return get_average_rating(mysql)

# if __name__ == '__main__':
#     app.run(debug=True)
