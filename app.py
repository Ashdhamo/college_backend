from flask import Flask, jsonify
import mysql.connector
from db_connector import get_db_connection, close_connection
from login.login import login_blueprint  
from student.student import student_blueprint
from professor.professor import professor_blueprint
from classes.classes import classes_blueprint
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(student_blueprint, url_prefix='/student')
app.register_blueprint(professor_blueprint, url_prefix='/professor')
app.register_blueprint(classes_blueprint, url_prefix='/classes')



if __name__ == '__main__':
    # Debug print to verify blueprints
    print("\nRegistered blueprints:", list(app.blueprints.keys()))
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(
                f"{rule.endpoint}: {rule.rule} [{','.join(sorted(rule.methods))}]"
            )

    app.run(host='0.0.0.0', port=8080, debug=True)
