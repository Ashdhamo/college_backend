from flask import Blueprint, request, jsonify
import mysql.connector
from db_connector import get_db_connection, close_connection

professor_blueprint = Blueprint('professor', __name__)



@professor_blueprint.route('/professor', methods=['GET'])
def get_professor():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries

        cursor.execute("SELECT * FROM professor;")
        professors = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(professors), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@professor_blueprint.route('/search', methods=['POST'])
def search_professor():
    try:           
        data = request.get_json()
        input_name = data.get('name', '').strip().lower()
        department= data.get('department')
        tenure= data.get('tenure')
        salary= data.get('salary')
        salaryValue= data.get('salaryValue')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 

        query = "SELECT * FROM professor WHERE 1=1"  # Ensures proper query building
        params = []

        if input_name:
            query += " AND LOWER(name) LIKE %s"
            params.append(f"%{input_name}%")

        if department:
            query += " AND LOWER(department) LIKE %s"
            params.append(f"%{department}%")

       
        if tenure in (0, 1):
            query += " AND tenure = %s"
            params.append(tenure)
        
        if salary == "greater":
            query += " AND salary > %s"
            params.append(salaryValue)
        elif salary == "less":
            query += " AND salary < %s"
            params.append(salaryValue)




        cursor.execute(query, params)  # Execute with parameters to prevent SQL injection
        professors = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(professors), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@professor_blueprint.route('/add', methods=['POST']) 
def add_professor():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        data = request.get_json()

        name = data.get('name')
        department = data.get('department')
        tenure = data.get('tenure')
        salary = data.get('salary')
        email = data.get('email')
        phone = data.get('phone')
        years_worked = data.get('years_worked')
               
        if not all([name, department, salary, email, phone, years_worked]) or tenure is None:
            return jsonify({'error': 'Missing required fields: name, department, tenure, salary, phone, years worked, or email'}), 400

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor WHERE email = %s", (email,))
        existing_professor = cursor.fetchone()
        if existing_professor:
            return jsonify({'error': 'Email already exists in professors table'}), 409
        cursor.execute("INSERT INTO professor (name, department, tenure, salary, email, phone, years_worked) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, department, tenure, salary, email, phone, years_worked))
        cursor.execute("SELECT ID FROM professor WHERE name = %s AND department = %s AND tenure = %s AND salary = %s AND email = %s AND phone = %s AND years_worked=%s", (name, department, tenure, salary, email, phone, years_worked))
        professorId = cursor.fetchone()
        username = "professor" + str(professorId[0])
        cursor.execute("INSERT INTO login_data (id, email,position, user_name) VALUES (%s, %s, %s, %s)", (professorId[0], email, "professor", username ))

        conn.commit()

        return jsonify({
            'message': 'professor added successfully'
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
       
@professor_blueprint.route('/<int:ID>', methods=['PATCH'])
def update_professor(ID):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        data = request.get_json()

        # Fields that can be updated
        fields = ['name', 'department', 'tenure', 'salary', 'email', 'phone', 'years_worked']
        updates = []
        values = []

        for field in fields:
            if field in data:
                updates.append(f"{field} = %s")
                values.append(data[field])

        if not updates:
            return jsonify({'error': 'No valid fields provided for update'}), 400

        # Check if email is being updated and already exists
        if 'email' in data:
            cursor.execute("SELECT * FROM professor WHERE email = %s AND ID != %s", (data['email'], ID))
            existing_professor = cursor.fetchone()
            if existing_professor:
                return jsonify({'error': 'Email already exists'}), 409

        # Construct the update query
        update_query = f"UPDATE professor SET {', '.join(updates)} WHERE ID = %s"
        cursor.execute(update_query, values + [ID])

        # Update email in login_data if email is changed
        if 'email' in data:
            cursor.execute("UPDATE login_data SET email = %s WHERE id = %s", (data['email'], ID))

        conn.commit()

        return jsonify({'message': 'Professor updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@professor_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_professor(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("DELETE FROM professor WHERE id= %s", (id,))
        cursor.execute("DELETE FROM login_data WHERE id= %s AND position =%s", (id, "professor"))
        conn.commit()

        return jsonify({'message': 'Professor deleted successfully'}), 200

    finally:
        cursor.close()
        conn.close()


    