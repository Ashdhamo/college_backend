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
        #year= data.get('year')
       # major= data.get('major')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 

        query = "SELECT * FROM professor WHERE 1=1"  # Ensures proper query building
        params = []

        if input_name:
            query += " AND LOWER(name) LIKE %s"
            params.append(f"%{input_name}%")

        # if major:
        #     query += " AND LOWER(major) LIKE %s"
        #     params.append(f"%{major}%")

        # # Add year filtering if provided
        # if year:
        #     if isinstance(year, list):  # If multiple years are provided
        #         placeholders = ','.join(['%s'] * len(year))  # Creates "%s,%s" for query
        #         query += f" AND year IN ({placeholders})"
        #         params.extend(year)
        #     else:  # If a single year is provided
        #         query += " AND year = %s"
        #         params.append(year)

        cursor.execute(query, params)  # Execute with parameters to prevent SQL injection
        professors = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(professors), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# @professor_blueprint.route('/add', methods=['POST'])
# def add_professor():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         data = request.get_json()

#         name = data.get('name')
#         year = data.get('year')
#         major = data.get('major')
#         email = data.get('email')
               
#         if not all([name, year, major, email]):
#             return jsonify({'error': 'Missing required fields: name, year, major, or email'}), 400

#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM professor WHERE email = %s", (email,))
#         existing_professor = cursor.fetchone()
#         if existing_professor:
#             return jsonify({'error': 'Email already exists in professors table'}), 409
#         cursor.execute("INSERT INTO professor (name, year, major, email) VALUES (%s, %s, %s, %s)", (name, year, major, email))
#         cursor.execute("SELECT ID FROM professor WHERE name = %s AND year = %s AND major = %s AND email = %s", (name, year, major, email))
#         professorId = cursor.fetchone()
#         username = "professor" + str(professorId[0])
#         cursor.execute("INSERT INTO login_data (id, email,position, user_name) VALUES (%s, %s, %s, %s)", (professorId[0], email, "professor", username ))

#         conn.commit()

#         return jsonify({
#             'message': 'professor added successfully'
#         }), 201

#     except Exception as e: 
#         conn.rollback()
#         return jsonify({'error': str(e)}), 500

#         #add name, email, year, major (no need to validate)


# @professor_blueprint.route('/<id>', methods=['DELETE'])
# def delete_professor(id):
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         cursor.execute("SELECT * FROM professor WHERE id = %s", (id,))
#         professor = cursor.fetchone()
#         if not professor:
#             cursor.close()
#             connection.close()
#             return jsonify({'error': 'professor not found'}), 404

        
#         # Delete the professor from the database
#         cursor.execute("DELETE FROM professor WHERE id = %s", (id,))
#         connection.commit()
#         cursor.execute("DELETE FROM login_data WHERE id = %s AND position = %s ", (id, "professor"))
#         connection.commit()

#         cursor.close()
#         connection.close()

#         return jsonify({'message': f'professor with ID {id} deleted successfully'}), 200

#     except Exception as e:
#         connection.rollback()
#         return jsonify({'error': str(e)}), 500

# @professor_blueprint.route('/<int:id>', methods=['PATCH'])
# def update_professor(id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         data = request.get_json()

#         # Fields that can be updated
#         fields = ['name', 'year', 'major', 'email']
#         updates = []
#         values = []

#         for field in fields:
#             if field in data:
#                 updates.append(f"{field} = %s")
#                 values.append(data[field])

#         if not updates:
#             return jsonify({'error': 'No valid fields provided for update'}), 400

#         # Check if email is being updated and already exists
#         if 'email' in data:
#             cursor.execute("SELECT * FROM professor WHERE email = %s AND ID != %s", (data['email'], id))
#             existing_professor = cursor.fetchone()
#             if existing_professor:
#                 return jsonify({'error': 'Email already exists'}), 409

#         # Construct the update query
#         update_query = f"UPDATE professor SET {', '.join(updates)} WHERE ID = %s"
#         cursor.execute(update_query, values + [id])

#         # Update email in login_data if email is changed
#         if 'email' in data:
#             cursor.execute("UPDATE login_data SET email = %s WHERE id = %s", (data['email'], id))

#         conn.commit()

#         return jsonify({'message': 'professor updated successfully'}), 200

#     except Exception as e:
#         conn.rollback()
#         return jsonify({'error': str(e)}), 500

#     finally:
#         cursor.close()
#         conn.close()
