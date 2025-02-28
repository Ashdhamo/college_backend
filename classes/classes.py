from flask import Blueprint, request, jsonify
import mysql.connector
from db_connector import get_db_connection, close_connection

classes_blueprint = Blueprint('classes', __name__)

@classes_blueprint.route('/add', methods=['POST'])
def addClass():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        data = request.get_json()
        class_name = data.get('class_name')
        professorID = data.get('professorID')
        units = data.get('units')
        seats = data.get('seats')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        schedule = data.get('schedule')  # Expecting a list of class days/times

        if None in [class_name, professorID, units, seats, start_date, end_date, schedule]:
            return jsonify({'error': 'Missing required fields'}), 400

        if not isinstance(schedule, list) or len(schedule) == 0:
            return jsonify({'error': 'Schedule must be a non-empty list'}), 400

        # Validate class_day
        valid_days = {'SAT', 'M', 'T', 'W', 'R', 'F', 'SUN'}
        for entry in schedule:
            if entry.get('class_day') not in valid_days:
                return jsonify({'error': f"Invalid class_day '{entry.get('class_day')}'. Must be one of SAT, M, T, W, R, F, SUN"}), 400
            if 'start_time' not in entry or 'end_time' not in entry:
                return jsonify({'error': 'Missing start_time or end_time in schedule'}), 400

        # Check if professor exists
        cursor.execute("SELECT * FROM professor WHERE id = %s", (professorID,))
        existing_professor = cursor.fetchone()
        if not existing_professor:
            return jsonify({'error': 'Professor does not exist'}), 409

        # Insert class
        cursor.execute(
            "INSERT INTO classes (class_name, professorID, units, seats, start_date, end_date) VALUES (%s,%s,%s,%s,%s,%s)",
            (class_name, professorID, units, seats, start_date, end_date)
        )
        conn.commit()

        # Get class_id of newly inserted class
        cursor.execute(
            "SELECT class_id FROM classes WHERE class_name = %s AND professorID = %s AND units = %s AND seats = %s AND start_date = %s AND end_date = %s",
            (class_name, professorID, units, seats, start_date, end_date)
        )
        class_record = cursor.fetchone()
        if not class_record:
            return jsonify({'error': 'Class insertion failed'}), 500

        class_id = class_record['class_id']

        # Insert multiple schedules for the class
        for entry in schedule:
            cursor.execute(
                "INSERT INTO class_schedule (class_id, class_day, start_time, end_time) VALUES (%s, %s, %s, %s)",
                (class_id, entry['class_day'], entry['start_time'], entry['end_time'])
            )

        conn.commit()

        return jsonify({'message': 'Class added successfully', 'class_id': class_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
