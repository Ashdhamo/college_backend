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
        year= data.get('year')
        major= data.get('major')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 

        query = "SELECT * FROM student WHERE 1=1"  # Ensures proper query building
        params = []

        # Add name filtering if provided
        if input_name:
            query += " AND LOWER(name) LIKE %s"
            params.append(f"%{input_name}%")

        if major:
            query += " AND LOWER(major) LIKE %s"
            params.append(f"%{major}%")

        # Add year filtering if provided
        if year:
            if isinstance(year, list):  # If multiple years are provided
                placeholders = ','.join(['%s'] * len(year))  # Creates "%s,%s" for query
                query += f" AND year IN ({placeholders})"
                params.extend(year)
            else:  # If a single year is provided
                query += " AND year = %s"
                params.append(year)

        cursor.execute(query, params)  # Execute with parameters to prevent SQL injection
        students = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(students), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@student_blueprint.route('/add', methods=['POST'])
def add_student():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        data = request.get_json()

        name = data.get('name')
        year = data.get('year')
        major = data.get('major')
        email = data.get('email')
        conn = get_db_connection()
               
        if not all([name, year, major, email]):
            return jsonify({'error': 'Missing required fields: name, year, major, or email'}), 400

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_student = cursor.fetchone()
        if existing_student:
            return jsonify({'error': 'Email already exists in Students table'}), 409
        cursor.execute("INSERT INTO student (name, year, major, email) VALUES (%s, %s, %s, %s)", (name, year, major, email))
        conn.commit()

        return jsonify({
            'message': 'Student added successfully'
        }), 201

    except Exception as e: 
        conn.rollback()
        return jsonify({'error': str(e)}), 500

        #add name, email, year, major (no need to validate)