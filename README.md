# Bookstore Management API

This project is a Flask-based RESTful API for managing a bookstore system. It provides endpoints for handling books, authors, users' shopping carts, and wishlists. The API is designed for easy integration with front-end applications and supports CRUD operations for various bookstore entities.

## Table of Contents

1. [Features](#features)
2. [Endpoints](#endpoints)
3. [Installation](#installation)
   - [How to (Mac)](#how-to-mac)
   - [How to (Windows)](#how-to-windows)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [Contributors](#contributors)
8. [License](#license)

## Features

This API supports the following features for the online bookstore application:

1. **Book Browsing and Sorting**: Allows users to browse and sort books by genre, retrieve top-sellers, and filter by rating. Additionally, admins can apply discounts by publisher.
2. **Profile Management**: Enables users to create and update profiles with personal information, add credit cards, and retrieve user data.
3. **Shopping Cart**: Allows users to add, view, and delete items from their shopping cart, as well as calculate the subtotal for items in the cart.
4. **Book Details**: Provides detailed information about each book, including creating book entries, fetching book details, and associating books with authors.
5. **Book Rating and Commenting**: Allows users to rate books on a 5-star scale, comment on books, retrieve comments, and see average ratings.
6. **Wishlist Management**: Users can create multiple wishlists, add/remove books from wishlists, and move books from wishlists to the shopping cart.

## Endpoints

### Books

- **GET /books**: Retrieve all books.
- **POST /create-book**: Add a new book.
- **GET /get-book/<isbn>**: Retrieve book details by ISBN.
- **GET /books_by_genre?genre=<genre>**: Retrieve books by genre.
- **PUT /books_discount_by_publisher?publisher=<publisher>&discount=<discount>**: Update book prices by publisher with a discount.

### Authors

- **POST /create-author**: Add or update an author.
- **GET /authors**: Retrieve all authors.
- **GET /get-books-by-author/<author_id>**: List books by a specific author.

### Shopping Cart

- **GET /shopping_cart?UserId=<user_id>**: Retrieve items in the user's shopping cart.
- **POST /shopping_cart**: Add a book to the user's cart.

### Wishlist

- **POST /wishlist**: Create a new wishlist for a user.
- **POST /wishlist/book**: Add a book to a wishlist.
- **DELETE /wishlist/book**: Remove a book from a wishlist and optionally add it to the shopping cart.
- **GET /wishlist/<wishlist_id>/books**: Retrieve all books in a wishlist.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JernaiBennett/Soft-Eng-Group-3
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the environment variables in a `.env` file:

   ```plaintext
   MYSQL_HOST=<your_mysql_host>
   MYSQL_USER=<your_mysql_user>
   MYSQL_PASSWORD=<your_mysql_password>
   MYSQL_DB=<your_database_name>
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### HOW TO MAC

1. `python3 -m pip install --user virtualenv` # Install virtualenv if you don’t have it
2. `python3 -m venv venv` # Create the virtual environment
3. `source venv/bin/activate` # Activate the virtual environment
4. `pip3 install -r requirements.txt` # Install all packages from the requirements.txt
5. `python3 main.py` # Run the application
6. `deactivate` # Deactivate the virtual environment if needed

### HOW TO Windows

1. `python -m pip install --user virtualenv` # Install virtualenv if you don’t have it
2. `python -m venv venv` # Create the virtual environment
3. `venv\Scripts\activate` # Activate the virtual environment
4. `pip install -r requirements.txt` # Install all packages from the requirements.txt
5. `python main.py` # Run the application
6. `deactivate` # Deactivate the virtual environment if needed

## Usage

After starting the server, use a tool like Postman or curl to interact with the API. The server will be running at `http://localhost:5000`.

## File Structure

- `main.py`: Main entry point for the API, contains route definitions and initializes the application.
- `ShoppingCart.py`: Contains functions to manage shopping cart operations, such as adding and retrieving books from a user's cart.
- `bookdetails.py`: Handles book and author-related operations, including adding books, retrieving book details, and managing authors.
- `Books.py`: Provides methods for retrieving books, filtering by genre, and updating book prices by applying discounts from specific publishers.
- `wishlistmanagement.py`: Manages wishlist functionality, including creating wishlists, adding/removing books, and transferring books from a wishlist to a shopping cart.

## Dependencies

- **Flask**: For creating the web server and handling API routes.
- **Flask-MySQLdb**: For connecting Flask to MySQL databases.
- **dotenv**: To load environment variables from a `.env` file.
- **MySQL Connector**: For wishlist management, enabling interactions with the MySQL database.

## Contributors

<div style="display: flex; flex-wrap: wrap; gap: 20px;">

<div style="text-align: center; width: 120px;">
    <img src="https://github.com/JernaiBennett.png" width="50" height="50"><br>
    <a href="https://github.com/JernaiBennett">Jernai Bennett</a><br>
    <small>Jernai Bennett</small>
</div>

<div style="text-align: center; width: 120px;">
    <img src="https://github.com/fflores0467.png" width="50" height="50"><br>
    <a href="https://github.com/fflores0467">fflores0467</a><br>
    <small>Francisco Flores</small>
</div>

<div style="text-align: center; width: 120px;">
    <img src="https://github.com/sandorh12.png" width="50" height="50"><br>
    <a href="https://github.com/sandorh12">sandorh12</a><br>
    <small>Sandor Hernandez</small>
</div>

<div style="text-align: center; width: 120px;">
    <img src="https://github.com/justinCastillo1446.png" width="50" height="50"><br>
    <a href="https://github.com/justinCastillo1446">justinCastillo1446</a><br>
    <small>Justin Castillo</small>
</div>

<div style="text-align: center; width: 120px;">
    <img src="https://github.com/NereidaRondon.png" width="50" height="50"><br>
    <a href="https://github.com/NereidaRondon">NereidaRondon</a><br>
    <small>Nereida Rondon</small>
</div>

</div>

## License

This project is licensed under the MIT License.
