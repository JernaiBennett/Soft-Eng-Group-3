# to run, type python bookdetails.py in terminal

# flask is the server
from flask import g, Flask, request, jsonify
# provides MySQL connection for Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from Books import get_books 

print("API is running")

app = Flask(__name__)

# Load the .env file
load_dotenv()

# Set MySQL configurations using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Route to get all books
@app.route('/books', methods=['GET'])
def books_route():
    return get_books(mysql)  # Call the function from book_routes.py

if __name__ == '__main__':
    app.run(debug=True)

# the route is the url that the server is listening to, use app variable
# @app.route('/')
# def home():
#     return "Home"

#GET retrieve 
# @app.route("/get-user/<user_id>", methods=["GET"])

# def get_user(user_id):
#   #declare mock data for access parameter
#   user_data = {
#     "user_id:": user_id,
#     "name": "John Doe",
#     "email": "john.doe@example.com"
#   }

#query parameter ex:'get-user/123?extra=hello world', extra is the query parameter
  # extra = request.args.get('extra')
  # #if extra is not None, add it to the user_data
  # if extra:
  #   user_data['extra'] = extra
  # #return the user_data as a json object
  # # #200 is the status code of a successful response
  # return jsonify(user_data), 200

# test it out, URL: http://127.0.0.1:5000/get-user/123?extra="hello"

#POST create 
# @app.route("/create-user", methods=["POST"])
# def create_user(): 
#   #receive data from the request 
#   data = request.get_json()
#   # add to database here somewhere
#   #return the data as a json object
#   return jsonify(data), 201

   
#PUT modify

#DELETE remove


