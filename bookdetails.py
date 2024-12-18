# to run, type python bookdetails.py in terminal

# flask is the server
from flask import Flask, request, jsonify


######################## ADD Book ########################

# POST route to create a new book

def create_book(mysql):
    try:
        # get the book data from the request body (JSON format)
        data = request.get_json()

        # extract individual fields from the JSON data
        isbn = data.get('isbn')
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        author_first_name = data.get('author_first_name')
        author_last_name = data.get('author_last_name')
        genre = data.get('genre')
        publisher_name = data.get('publisher_name')
        year_published = data.get('year_published')
        copies_sold = data.get('copies_sold')

        # check if all required fields are present
        if not all([isbn, name, price, author_first_name, author_last_name, genre, publisher_name, year_published]):
            return jsonify({"error": "Missing required book data"}), 400

        # create a cursor object to execute the SQL query
        cur = mysql.connection.cursor()

        # Check if the author already exists in the Author table
        author_query = "SELECT id FROM Author WHERE first_name = %s AND last_name = %s"
        cur.execute(author_query, (author_first_name, author_last_name))
        author = cur.fetchone()

        # If the author doesn't exist, insert the new author and get the new author_id
        if not author:
            insert_author_query = "INSERT INTO Author (first_name, last_name) VALUES (%s, %s)"
            cur.execute(insert_author_query, (author_first_name, author_last_name))
            mysql.connection.commit()
            # Get the newly inserted author_id
            author_id = cur.lastrowid  
        # If the other DOES exist, get the existing author_id    
        else:
            author_id = author[0]  

        # Check if the publisher already exists in the Publisher table
        publisher_query = "SELECT id FROM Publisher WHERE name = %s"
        cur.execute(publisher_query, (publisher_name,))
        publisher = cur.fetchone()
        
        # If the publisher doesn't exist, insert the new publisher and get the new publisher_id
        if not publisher:
            
            insert_publisher_query = "INSERT INTO Publisher (name) VALUES (%s)"
            cur.execute(insert_publisher_query, (publisher_name,))
            mysql.connection.commit()
            # Get the newly inserted publisher_id
            publisher_id = cur.lastrowid  
        # Or get the existing publisher_id
        else:
            publisher_id = publisher[0]  

        # Insert the book into the Book table
        insert_book_query = """
            INSERT INTO Book (isbn, name, description, price, author_id, genre, publisher_id, year_published, copies_sold)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # execute the query with the provided book data
        cur.execute(insert_book_query, (isbn, name, description, price, author_id, genre, publisher_id, year_published, copies_sold))

        # commit the transaction
        mysql.connection.commit()

        # close the cursor
        cur.close()

        # return a success response
        return jsonify({"message": "Book added successfully!"}), 201

    except Exception as e:
        # return an error message in case of an exception
        return jsonify({"error": str(e)}), 500
    
#################### GET Book by ISBN ####################
# GET route to retrieve book by ISBN
# the route is the url that the server is listening to

def get_book(mysql, isbn):
    try:
        # create a cursor object to execute queries
        cur = mysql.connection.cursor()
        
        # SQL query to fetch the book details by ISBN
        query = "SELECT * FROM Book WHERE isbn = %s"
        
        # execute the query with the provided ISBN
        cur.execute(query, (isbn,))
        
        # fetch one result (assuming ISBN is unique)
        book = cur.fetchone()
        
        # if book is not found, return a 404 response
        if not book:
            return jsonify({"error": "Book not found"}), 404
        
        # otherwise, return the book details as JSON
        book_data = {
            "isbn": book[0],
            "name": book[1],
            "description": book[2],
            "price": book[3],
            "author_id": book[4],
            "genre": book[5],
            "publisher_id": book[6],
            "year_published": book[7],
            "copies_sold": book[8]
        }

        return jsonify(book_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
    

#################### CREATE Author profile ####################

# POST route to create a new author
def create_author(mysql):
    try:
        # Get the author data from the request body (JSON format)
        data = request.get_json()

        # Extract individual fields from the JSON data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        biography = data.get('biography')
        publisher_name = data.get('publisher_name')  # Changed to handle publisher_name instead of publisher_id

        # Check if both first_name and last_name are provided
        if not all([first_name, last_name]):
            return jsonify({"error": "First name and last name are required"}), 400

        # Create a cursor object to execute SQL queries
        cur = mysql.connection.cursor()

        # Step 1: Check if the publisher already exists in the Publisher table
        publisher_query = "SELECT id FROM Publisher WHERE name = %s"
        cur.execute(publisher_query, (publisher_name,))
        publisher = cur.fetchone()

        if publisher:
            # If the publisher exists, get the publisher_id
            publisher_id = publisher[0]
        else:
            # If the publisher does not exist, insert the publisher and get the new publisher_id
            insert_publisher_query = "INSERT INTO Publisher (name) VALUES (%s)"
            cur.execute(insert_publisher_query, (publisher_name,))
            mysql.connection.commit()
            publisher_id = cur.lastrowid

        # Step 2: Check if the author already exists in the database
        author_query = "SELECT id, biography, publisher_id FROM Author WHERE first_name = %s AND last_name = %s"
        cur.execute(author_query, (first_name, last_name))
        author = cur.fetchone()

        # If the author exists, update missing fields
        if author:
            author_id = author[0]
            existing_biography = author[1]
            existing_publisher_id = author[2]

            # Update the biography if it's missing or NULL
            if not existing_biography and biography:
                update_biography_query = "UPDATE Author SET biography = %s WHERE id = %s"
                cur.execute(update_biography_query, (biography, author_id))

            # Update the publisher_id if it's missing or NULL
            if not existing_publisher_id and publisher_id:
                update_publisher_query = "UPDATE Author SET publisher_id = %s WHERE id = %s"
                cur.execute(update_publisher_query, (publisher_id, author_id))

            mysql.connection.commit()

            return jsonify({"message": "Author information updated successfully!"}), 200

        # If the author does not exist, insert the new author
        else:
            if not biography:
                return jsonify({"error": "Biography is required for new authors"}), 400

            insert_author_query = """
                INSERT INTO Author (first_name, last_name, biography, publisher_id)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(insert_author_query, (first_name, last_name, biography, publisher_id))
            mysql.connection.commit()

            return jsonify({"message": "Author added successfully!"}), 201

    except Exception as e:
        # Return an error message in case of an exception
        return jsonify({"error": str(e)}), 500

    finally:
        # Close the cursor
        cur.close()

    
#################### GET List of books by Author ####################

# GET route to retrieve all books by a specific author

def get_books_by_author(mysql, author_id):
    try:
        # Create a cursor object to execute the query
        cur = mysql.connection.cursor()

        # SQL query to fetch all books where the author_id matches the given ID
        query = "SELECT isbn, name, description, price, genre, year_published, copies_sold FROM Book WHERE author_id = %s"

        # Execute the query with the given author_id
        cur.execute(query, (author_id,))

        # Fetch all the books returned by the query
        books = cur.fetchall()

        # If no books are found, return a 404 response
        if not books:
            return jsonify({"error": "No books found for this author"}), 404

        # Create a list to store book details
        book_list = []
        for book in books:
            book_data = {
                "isbn": book[0],
                "name": book[1],
                "description": book[2],
                "price": book[3],
                "genre": book[4],
                "year_published": book[5],
                "copies_sold": book[6]
            }
            book_list.append(book_data)

        # Return the list of books in JSON format
        return jsonify(book_list), 200

    except Exception as e:
        # Return an error message in case of an exception
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()

#################### BONUS METHOD to see Author ID numbers ####################

# GET route to retrieve a list of all authors with their IDs

def get_authors(mysql):
    try:
        # Create a cursor object to execute the query
        cur = mysql.connection.cursor()

        # SQL query to fetch all authors and their IDs
        query = "SELECT id, first_name, last_name FROM Author"

        # Execute the query
        cur.execute(query)

        # Fetch all the authors returned by the query
        authors = cur.fetchall()

        # If no authors are found, return a 404 response
        if not authors:
            return "No authors found", 404

        # Create a list to store author details
        author_text_list = []
        for author in authors:
            author_text_list.append(f"{author[0]} {author[1]} {author[2]}")

        # Join all author details with newline and return as plain text
        return "\n".join(author_text_list), 200

    except Exception as e:
        # Return an error message in case of an exception
        return str(e), 500

    finally:
        cur.close()

##############################################################




