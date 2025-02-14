import mysql.connector
from mysql.connector import Error
from typing import Optional

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='ash',
            password='ash-password',
            database='college_interface',
        )
        
        if connection.is_connected():
            return connection
        else:
            raise Error("Failed to establish database connection")

    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        raise

def close_connection(connection: Optional[mysql.connector.connection.MySQLConnection]) -> None:
    """
    Safely closes the database connection.
    """
    if connection and connection.is_connected():
        connection.close()

def test_connection():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("Database connection successful!")
            close_connection(conn)
            return True
    except Error as e:
        print(f"Error testing database connection: {e}")
        return False

if __name__ == "__main__":
    test_connection()
