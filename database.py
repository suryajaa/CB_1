import sqlite3

DB_NAME = "Users.db" #name of database


def connect_database(): #Connect to database
    connection = sqlite3.connect(DB_NAME)
    print("Connected to database")
    return connection


def initialize(): #Initialize database
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Users(
                   employee_no TEXT PRIMARY KEY,
                   password TEXT NOT NULL,
                   role TEXT NOT NULL
                   )
                   """)
    connection.commit()
    connection.close()


def add_user(employee_no,hashed_password,role): #New user registers
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (employee_no,password,role) values(?,?,?)",(employee_no,hashed_password,role))
    connection.commit()
    connection.close()


def get_user(employee_no): #Fetches the user's employee number while logging in
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("SELECT password,role FROM Users where employee_no = ?",(employee_no,))
    user = cursor.fetchone()
    connection.close()
    return user
    

def user_exists(employee_no): #Checks if the user has already registered
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Users where employee_no = ?",(employee_no,))
    exists = cursor.fetchone() is not None
    connection.close()
    return exists

