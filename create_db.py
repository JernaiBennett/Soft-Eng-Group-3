import mysql.connector
#crete connection to the database
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="database@1984",
  auth_plugin='mysql_native_password'
)
#cursor is used to interact with the database
my_cursor = conn.cursor()

#execute the query to create a database
#COMMENTED LINE 14 TO AVOID CREATING A DATABASE EVERYTIME THIS FILE IS RUN
#my_cursor.execute("CREATE DATABASE bookstore")

my_cursor.execute("SHOW DATABASES")

#loop through the databases and print them
for db in my_cursor:
  print(db)

 # to run this file, open a terminal and type: python create_db.py 