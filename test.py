import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("root")
db_password = os.getenv("password")
db_host = os.getenv("localhost")
db_name = os.getenv("classicmodels")

# Test connection
try:
    conn = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print(f"Tables in the database: {tables}")
    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")
