import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_rental_mobil"
        )
        return conn
    except Error as e:
        print(f"Gagal konek ke database: {e}")
        return None