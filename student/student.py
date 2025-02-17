from flask import Blueprint, request, jsonify
import mysql.connector
from db_connector import get_db_connection, close_connection

student_blueprint = Blueprint('student', __name__)



@student_blueprint.route('/student', methods=['GET'])
def get_student():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries

        cursor.execute("SELECT * FROM student;")
        students = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(students), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@student_blueprint.route('/search', methods=['POST'])
def search_student():
    try:           
        data = request.get_json()
        input_name = data.get('name', '').strip().lower()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 

        if not input_name:
            cursor.execute("SELECT * FROM student;")
            students = cursor.fetchall()
        else:    

            #initially I put input_name but it would literally search input_name 
            query="SELECT * FROM student WHERE LOWER(name) LIKE %s;"
            cursor.execute(query, (f"%{input_name}%",))
            students = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(students), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500