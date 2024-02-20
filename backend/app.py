from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'mysecret1234' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 
jwt = JWTManager(app)


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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (role_id) REFERENCES roles (id),
            UNIQUE (user_id, role_id)
        )
    ''')
    conn.commit()
    conn.close()

# Creating the tables
create_tables()

PREDEFINED_ROLES = ['admin', 'user', 'librarian']

def create_predefined_roles():
    conn = get_db_connection()
    cursor = conn.cursor()
    for role in PREDEFINED_ROLES:
        try:
            cursor.execute('''
                INSERT INTO roles (role_name) VALUES (?)
            ''', (role,))
        except IntegrityError:
            # Role already exists, skip
            pass
    conn.commit()
    conn.close()

# def assign_admin_role(user_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT role_id FROM user_roles WHERE user_id = ? AND role_id = (
#             SELECT id FROM roles WHERE role_name = 'admin'
#         )
#     ''', (user_id,))
#     existing_admin_role = cursor.fetchone()
#     if not existing_admin_role:
#         cursor.execute('''
#             INSERT INTO user_roles (user_id, role_id) VALUES (?, (
#                 SELECT id FROM roles WHERE role_name = 'admin'
#             ))
#         ''', (user_id,))
#         conn.commit()
#     conn.close()


def find_user_by_email_and_name(email, name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ? AND name = ?
    ''', (email, name))
    user = cursor.fetchone()
    conn.close()
    return user

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
        user_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO user_roles (user_id, role_id) 
            SELECT ?, id FROM roles WHERE role_name = 'user'
        ''', (user_id,))
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
        if user and user['email'] == email and user['password'] == password:
            access_token = create_access_token(identity=user['id'])
            return jsonify({"access_token": access_token, "message": "User logged in successfully"})
    else:
        return jsonify({"error": "Invalid email or password"}), 400
    
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if the user has admin privileges
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users 
        INNER JOIN user_roles ON users.id = user_roles.user_id
        INNER JOIN roles ON user_roles.role_id = roles.id
        WHERE email = ? AND password = ? AND role_name = 'admin'
    ''', (email, password))
    admin_user = cursor.fetchone()
    conn.close()

    if admin_user:
        access_token = create_access_token(identity=admin_user['id'])
        return jsonify({"access_token": access_token, "message": "Admin logged in successfully", "admin_name": admin_user['name']})
    else:
        return jsonify({"error": "Invalid admin credentials"}), 401
    
@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users 
        INNER JOIN user_roles ON users.id = user_roles.user_id
        INNER JOIN roles ON user_roles.role_id = roles.id
        WHERE users.id = ? AND role_name = 'admin'
    ''', (current_user_id,))
    admin_user = cursor.fetchone()
    conn.close()

    if admin_user:
        # Fetch all users from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT users.id, users.name, users.email, roles.role_name
            FROM users
            LEFT JOIN user_roles ON users.id = user_roles.user_id
            LEFT JOIN roles ON user_roles.role_id = roles.id
        ''')
        users = cursor.fetchall()
        conn.close()
        
        # Converting into a json type
        users_list = []
        for user in users:
            users_list.append({
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role_name']
            })
        return jsonify(users_list)
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    
@app.route('/api/admin/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
def update_user_role(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_roles
            INNER JOIN roles ON user_roles.role_id = roles.id
            WHERE user_id = ? AND role_name = 'admin'
        ''', (current_user_id,))
        admin_user = cursor.fetchone()
        conn.close()

        if admin_user:
            data = request.json
            new_role = data.get('role')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_roles
                SET role_id = (SELECT id FROM roles WHERE role_name = ?)
                WHERE user_id = ?
            ''', (new_role, user_id))
            conn.commit()
            conn.close()

            return jsonify({"message": "User role updated successfully"}), 200
        else:
            return jsonify({"error": "Unauthorized access"}), 401
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    
@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM user_roles
            INNER JOIN roles ON user_roles.role_id = roles.id
            WHERE user_id = ? AND role_name = 'admin'
        ''', (current_user_id,))
        admin_user = cursor.fetchone()
        conn.close()

        if admin_user:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM users WHERE id = ?
            ''', (user_id,))
            conn.commit()
            conn.close()

            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "Unauthorized access"}), 401
    else:
        return jsonify({"error": "Unauthorized access"}), 401



if __name__ == '__main__':
    create_predefined_roles()
    # targetUser = find_user_by_email_and_name("palindrajit10@gmail.com", "indrajit")
    # if targetUser:
    #     assign_admin_role(targetUser['id'])
    #     print("Admin role assigned to user:", targetUser['name'])
    # else:
    #     print("No user found with such information [Note that the username and email is case sensitive].")
    
    app.run(debug=True)
