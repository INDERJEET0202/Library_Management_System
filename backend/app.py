from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import IntegrityError

app = Flask(__name__)
CORS(app)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create tables in the database
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create tables when the Flask application starts
create_tables()

@app.route('/')
def hello():
    return 'Hello from backend!'

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password) VALUES (?, ?, ?)
        ''', (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User signed up successfully"})
    except IntegrityError:
        conn.rollback()
        conn.close()
        return jsonify({"error": "User with this email already exists"}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND password = ?
    ''', (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "User logged in successfully"})
    else:
        return jsonify({"error": "Invalid email or password"}), 400

if __name__ == '__main__':
    app.run(debug=True)
