######################## Get All Books ########################

from flask import jsonify
from flask_mysqldb import MySQL

# Function to get all books
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
