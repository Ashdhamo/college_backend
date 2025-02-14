from flask import Blueprint, request, jsonify
import mysql.connector
from db_connector import get_db_connection, close_connection

login_blueprint = Blueprint('login', __name__)



@login_blueprint.route('/login', methods=['POST'])
def login():
    try:
        
        data = request.get_json()
        username = data.get('username') 
        password = data.get('password')
        if username is None or password is None:
            return jsonify({'error': 'Username and password are required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM login_data WHERE user_name = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        close_connection(connection)

        if user:
            return jsonify({"message": "Login successful", "user": user}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500
