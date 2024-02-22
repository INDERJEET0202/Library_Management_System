from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask import g
from datetime import datetime


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'mysecret1234' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 
jwt = JWTManager(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles (id),
            UNIQUE (user_id, role_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_created TEXT,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT,
            authors TEXT,
            date_issued TEXT,
            return_date TEXT,
            rating INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS section_books (
            book_id INTEGER,
            section_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (section_id) REFERENCES sections (id),
            UNIQUE (book_id, section_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books_allocation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            section_id INTEGER,
            user_id INTEGER,
            is_allocated INTEGER,
            is_requested INTEGER,
            date_of_issue TEXT,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (section_id) REFERENCES sections (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            feedback TEXT,
            returned INTEGER,
            date_of_issue TEXT,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')


    conn.commit()
    conn.close()

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

def verify_user_role(user_id, role_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM user_roles
        INNER JOIN roles ON user_roles.role_id = roles.id
        WHERE user_id = ? AND role_name = ?
    ''', (user_id, role_name))
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

    # TODO: Librarian and admin cannot login here. Librarian and admin have separate login endpoints

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
            return jsonify({"access_token": access_token, "message": "User logged in successfully", "userName": user['name']})
    else:
        return jsonify({"error": "Invalid email or password"}), 400
    
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

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
    admin_user = verify_user_role(current_user_id, 'admin')

    if admin_user:
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
    admin_user = verify_user_role(current_user_id, 'admin')

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
    
@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    admin_user = verify_user_role(current_user_id, 'admin')

    if admin_user:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users WHERE id = ?
        ''', (user_id,))
        cursor.execute('''
            DELETE FROM user_roles WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@app.route('/api/librarian/login', methods=['POST'])
def librarian_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE email = ? AND password = ?
    ''', (email, password, ))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_id = user['id']
        librarian_user = verify_user_role(user_id, 'librarian')
        if librarian_user:
            access_token = create_access_token(identity=user_id)
            return jsonify({"access_token": access_token, "message": "Librarian logged in successfully"})
        else:
            return jsonify({"error": "Invalid librarian credentials"}), 401
    else:
        return jsonify({"error": "Invalid email or password"}), 400
    

@app.route('/api/add/new-section', methods=['POST'])
@jwt_required()
def add_new_section():
    data = request.json
    name = data.get('title')
    date_created = data.get('date')
    description = data.get('description')

    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')

    if user:
        conn = get_db_connection();
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO sections (name, date_created, description) VALUES (?, ?, ?)
            ''', (name, date_created, description))
            conn.commit()
            conn.close()
            return jsonify({"message": "Section added successfully"}), 200
        except IntegrityError:
            return jsonify({"error": "Section with the provided name already exists"}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred while adding the section: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@app.route('/api/sections', methods=['GET'])
@jwt_required()
def get_all_sections():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')
    
    if user:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sections')
            sections = cursor.fetchall()
            conn.close()

            sections_list = []
            for section in sections:
                sections_list.append({
                    'id': section['id'],
                    'name': section['name'],
                    'date_created': section['date_created'],
                    'description': section['description']
                })

            return jsonify(sections_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching sections: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    
@app.route('/api/add/book', methods=['POST'])
@jwt_required()
def add_new_book():
    pass
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')

    if user:
        try:
            data = request.json
            title = data.get('title')
            authorName = data.get('authorName')
            content = data.get('content')
            section = data.get('section')
            date_issued = str(datetime.now().strftime('%Y-%m-%d'))
            return_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d') 
            rating = 0

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM sections WHERE name = ?', (section,))
            section_id = cursor.fetchone()['id']
            conn.close()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (name, content, authors, date_issued, return_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, authorName, date_issued, return_date))
            book_id = cursor.lastrowid
            conn.commit()

            cursor.execute('''
                INSERT INTO section_books (book_id, section_id)
                VALUES (?, ?)
            ''', (book_id, section_id))
            conn.commit()
            conn.close()

            return jsonify({"message": "Book added successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while adding the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@app.route('/api/books', methods=['GET'])
@jwt_required()
def get_all_books():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'user')

    if user:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT books.id, books.name as book_name, books.content, books.authors, books.date_issued, books.return_date, books.rating,
                sections.name as section_name,
                CASE 
                    WHEN ba.is_allocated = 1 THEN 1
                    ELSE 0
                END as allocated,
                CASE 
                    WHEN ba.is_requested = 1 AND ba.user_id = ? THEN 1
                    ELSE 0
                END as requested
                FROM books
                INNER JOIN section_books ON books.id = section_books.book_id
                INNER JOIN sections ON section_books.section_id = sections.id
                LEFT JOIN books_allocation ba ON books.id = ba.book_id
            ''', (current_user_id,))
            books = cursor.fetchall()
            conn.close()

            books_list = []
            for book in books:
                books_list.append({
                    'id': book['id'],
                    'name': book['book_name'],
                    'content': book['content'],
                    'authors': book['authors'],
                    'date_issued': book['date_issued'],
                    'return_date': book['return_date'],
                    'rating': book['rating'],
                    'section': book['section_name'],
                    'allocated': book['allocated'],
                    'requested': book['requested']
                })

            return jsonify(books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401



@app.route('/api/request/book', methods=['POST'])
@jwt_required()
def request_book():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'user')

    if user:
        try:
            data = request.json
            book_id = data.get('book_id')
            section_name = data.get('section_name')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM books_allocation WHERE book_id = ?
            ''', (book_id,))
            book_allocation = cursor.fetchone()

            if book_allocation:
                if book_allocation['is_allocated'] == 1:
                    conn.close()
                    return jsonify({"error": "This book is already allocated to someone"}), 400
                else:
                    cursor.execute('''
                        SELECT * FROM books_allocation WHERE book_id = ? AND is_requested = 1 AND user_id != ?
                    ''', (book_id, current_user_id))
                    existing_request = cursor.fetchone()
                    
                    if existing_request:
                        cursor.execute('''
                            INSERT INTO books_allocation (book_id, section_id, user_id, is_allocated, is_requested, date_of_issue, return_date)
                            VALUES (?, (SELECT id FROM sections WHERE name = ?), ?, 0, 1, ?, ?)
                        ''', (book_id, section_name, current_user_id, datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')))
                        conn.commit()
                        conn.close()
                        return jsonify({"message": "Book requested successfully"}), 200
                    else:
                        cursor.execute('''
                            UPDATE books_allocation
                            SET section_id = (SELECT id FROM sections WHERE name = ?),
                                user_id = ?,
                                is_allocated = 0,
                                is_requested = 1,
                                date_of_issue = ?,
                                return_date = ?
                            WHERE book_id = ?
                        ''', (section_name, current_user_id, datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), book_id))
            else:
                cursor.execute('''
                    INSERT INTO books_allocation (book_id, section_id, user_id, is_allocated, is_requested, date_of_issue, return_date)
                    VALUES (?, (SELECT id FROM sections WHERE name = ?), ?, 0, 1, ?, ?)
                ''', (book_id, section_name, current_user_id, datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')))
            conn.commit()
            conn.close()

            return jsonify({"message": "Book requested successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while processing the request: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@app.route('/api/books/requested', methods=['GET'])
@jwt_required()
def requested_books():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')
    if user:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT books_allocation.id AS allocation_id, books.id AS book_id, books.name AS book_name, sections.id AS section_id, sections.name AS section_name, users.id AS user_id, users.name AS user_name
                FROM books_allocation
                INNER JOIN books ON books_allocation.book_id = books.id
                INNER JOIN sections ON books_allocation.section_id = sections.id
                INNER JOIN users ON books_allocation.user_id = users.id
                WHERE books_allocation.is_requested = 1
            ''')
            requested_books = cursor.fetchall()
            conn.close()

            requested_books_list = []
            for book in requested_books:
                requested_books_list.append({
                    'allocation_id': book['allocation_id'],
                    'book_id': book['book_id'],
                    'book_name': book['book_name'],
                    'section_id': book['section_id'],
                    'section_name': book['section_name'],
                    'user_id': book['user_id'],
                    'user_name': book['user_name']
                })

            return jsonify(requested_books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching requested books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@app.route('/api/books/allocate', methods=['POST'])
@jwt_required()
def allocate_book():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')

    if user:
        try:
            data = request.json
            book_id = data.get('book_id')
            section_id = data.get('section_id')
            user_id = data.get('user_id')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE books_allocation
                SET is_allocated = 1,
                    is_requested = 0,
                    date_of_issue = ?,
                    return_date = ?
                WHERE book_id = ? AND section_id = ? AND user_id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), book_id, section_id, user_id))
            conn.commit()

            cursor.execute('''
                INSERT INTO user_books (user_id, book_id, date_of_issue, return_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, book_id, datetime.now().strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')))
            conn.commit()

            conn.close()

            return jsonify({"message": "Book allocated successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while allocating the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    
@app.route('/api/fetch_my_books', methods=['GET'])
@jwt_required()
def fetch_my_books():
    current_user_id = get_jwt_identity()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT books.id AS book_id, 
                   books.name AS book_title, 
                   books.authors AS author, 
                   books.content AS content,
                   sections.name AS section, 
                   books_allocation.id AS allocation_id, 
                   books_allocation.user_id AS user_id
            FROM books_allocation
            INNER JOIN books ON books_allocation.book_id = books.id
            INNER JOIN sections ON books_allocation.section_id = sections.id
            WHERE books_allocation.is_allocated = 1
        ''')
        books = cursor.fetchall()
        conn.close()

        books_list = []
        for book in books:
            if book['user_id'] == current_user_id:
                books_list.append({
                    'book_id': book['book_id'],
                    'book_title': book['book_title'],
                    'author': book['author'],
                    'content': book['content'],
                    'section': book['section'],
                    'allocation_id': book['allocation_id'],
                    'userId': book['user_id'] 
                })

        return jsonify(books_list), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching books: " + str(e)}), 500



@app.route('/api/return/book', methods=['POST'])
@jwt_required()
def return_book():
    current_user_id = get_jwt_identity()
    data = request.json
    allocation_id = data.get('allocation_id')
    book_id = data.get('book_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            DELETE FROM books_allocation WHERE id = ? AND user_id = ?
        ''', (allocation_id, current_user_id))
        
        cursor.execute('''
            UPDATE user_books SET returned = 1, return_date = ? 
            WHERE user_id = ? AND book_id = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), current_user_id, book_id))

        conn.commit()
        conn.close()

        return jsonify({"message": "Book returned successfully"}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": "An error occurred while returning the book: " + str(e)}), 500
    
@app.route('/api/fetch_returned_books', methods=['GET'])
@jwt_required()
def fetch_returned_books():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'user')
    if user:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT books.name AS book_title, books.authors AS author, sections.name AS section
                FROM user_books
                INNER JOIN books ON user_books.book_id = books.id
                INNER JOIN sections ON sections.id = (SELECT section_id FROM section_books WHERE book_id = user_books.book_id LIMIT 1)
                WHERE user_books.user_id = ? AND user_books.returned = 1
            ''', (current_user_id,))
            returned_books = cursor.fetchall()
            conn.close()

            returned_books_list = []
            for book in returned_books:
                returned_books_list.append({
                    'book_title': book['book_title'],
                    'author': book['author'],
                    'section': book['section']
                })

            return jsonify(returned_books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching returned books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@app.route('/api/delete/request', methods=['DELETE'])
@jwt_required()
def delete_request():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')
    if user:
        try:
            allocation_id = request.json.get('allocation_id') 
            if allocation_id is None:
                return jsonify({"error": "Allocation ID is missing from request body"}), 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM books_allocation WHERE id = ?
            ''', (allocation_id,))
            conn.commit()
            conn.close()

            return jsonify({"message": "Request deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while deleting the request: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    
@app.route('/api/librarian/allocated_books', methods=['GET'])
@jwt_required()
def get_allocated_books():
    current_user_id = get_jwt_identity()
    librarian = verify_user_role(current_user_id, 'librarian')

    if librarian:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ba.id AS allocation_id,
                       ba.book_id,
                       ba.user_id,
                       users.name AS user_name,
                       books.name AS book_name,
                       sections.name AS section_name
                FROM books_allocation AS ba
                INNER JOIN users ON ba.user_id = users.id
                INNER JOIN books ON ba.book_id = books.id
                INNER JOIN sections ON ba.section_id = sections.id
                WHERE ba.is_allocated = 1
            ''')
            allocated_books = cursor.fetchall()
            conn.close()

            allocated_books_list = []
            for book in allocated_books:
                allocated_books_list.append({
                    'allocation_id': book['allocation_id'],
                    'book_id': book['book_id'],
                    'user_id': book['user_id'],
                    'user_name': book['user_name'],
                    'book_name': book['book_name'],
                    'section_name': book['section_name']
                })

            return jsonify(allocated_books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching allocated books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401


@app.route('/api/fetch/section/books', methods=['POST'])
@jwt_required()
def fetchSection_books():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')
    if user:
        try:
            data = request.json
            section_id = data.get('section_id')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT books.id AS book_id, books.name AS book_name, books.authors AS author, sections.name AS section
                FROM books
                INNER JOIN section_books ON books.id = section_books.book_id
                INNER JOIN sections ON section_books.section_id = sections.id
                WHERE sections.id = ?
            ''', (section_id,))
            books = cursor.fetchall()
            conn.close()

            books_list = []
            for book in books:
                books_list.append({
                    'book_id': book['book_id'],
                    'book_name': book['book_name'],
                    'author': book['author'],
                    'section': book['section']
                })

            return jsonify(books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    
@app.route('/api/books/delete', methods=['DELETE'])
@jwt_required()
def delete_book():
    curr_user_id = get_jwt_identity()
    user = verify_user_role(curr_user_id, 'librarian')
    if user:
        try:
            book_id = request.json.get('book_id')
            if book_id is None:
                return jsonify({"error": "Book ID is missing from request body"}), 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM books WHERE id = ?
            ''', (book_id,))
            cursor.execute('''
                DELETE FROM books_allocation WHERE book_id = ?
            ''', (book_id,))
            cursor.execute('''
                DELETE FROM section_books WHERE book_id = ?
            ''', (book_id,))

            conn.commit()
            conn.close()

            return jsonify({"message": "Book deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while deleting the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    

@app.route('/api/revoke/book', methods=['POST'])
@jwt_required()
def revoke_book():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')
    data = request.json
    allocation_id = data.get('allocation_id')
    book_id = data.get('book_id')
    user_id = data.get('user_id')

    if user:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                DELETE FROM books_allocation WHERE id = ? AND user_id = ?
            ''', (allocation_id, user_id))
            
            cursor.execute('''
                UPDATE user_books SET returned = 1, return_date = ? 
                WHERE user_id = ? AND book_id = ?
            ''', (datetime.now().strftime('%Y-%m-%d'), user_id, book_id))

            conn.commit()
            conn.close()

            return jsonify({"message": "Book returned successfully"}), 200
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({"error": "An error occurred while returning the book: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401
    

@app.route('/api/fetch/librarian/books', methods=['GET'])
@jwt_required()
def fetch_all_books():
    current_user_id = get_jwt_identity()
    user = verify_user_role(current_user_id, 'librarian')
    
    if user:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT b.id AS book_id, 
                       b.name AS book_name, 
                       b.authors AS authors, 
                       s.name AS section_name,
                       CASE 
                           WHEN ba.is_allocated = 1 THEN 'allocated'
                           WHEN ba.is_requested = 1 THEN 'requested'
                           ELSE 'available' 
                       END AS status
                FROM books AS b
                LEFT JOIN (
                    SELECT book_id,
                           MAX(CASE WHEN is_allocated = 1 THEN 1 ELSE 0 END) AS is_allocated,
                           MAX(CASE WHEN is_requested = 1 THEN 1 ELSE 0 END) AS is_requested
                    FROM books_allocation
                    GROUP BY book_id
                ) AS ba ON b.id = ba.book_id
                LEFT JOIN section_books AS sb ON b.id = sb.book_id
                LEFT JOIN sections AS s ON sb.section_id = s.id
            ''')
            books = cursor.fetchall()
            conn.close()

            books_list = []
            for book in books:
                books_list.append({
                    'book_id': book['book_id'],
                    'book_name': book['book_name'],
                    'authors': book['authors'],
                    'section_name': book['section_name'],
                    'status': book['status']
                })

            return jsonify(books_list), 200
        except Exception as e:
            return jsonify({"error": "An error occurred while fetching books: " + str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized access"}), 401

@app.route('/api/books/issued-count', methods=['GET'])
def books_issued_count():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date_of_issue, COUNT(*) AS issued_count
        FROM user_books
        GROUP BY date_of_issue
    ''')
    issued_count_data = cursor.fetchall()
    conn.close()    

    issued_count_list = []
    for entry in issued_count_data:
        issued_count_list.append({
            'date_of_issue': entry['date_of_issue'],
            'issued_count': entry['issued_count']
        })

    return jsonify(issued_count_list), 200
    

@app.route('/api/books-per-section', methods=['GET'])
def books_per_section():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sections.name AS section_name, COUNT(*) AS books_count
        FROM section_books
        INNER JOIN sections ON section_books.section_id = sections.id
        GROUP BY section_books.section_id
    ''')
    books_per_section_data = cursor.fetchall()
    conn.close()

    books_per_section_list = []
    for entry in books_per_section_data:
        books_per_section_list.append({
            'section_name': entry['section_name'],
            'books_count': entry['books_count']
        })

    return jsonify(books_per_section_list), 200

if __name__ == '__main__':
    create_predefined_roles()
    # targetUser = find_user_by_email_and_name("palindrajit10@gmail.com", "indrajit")
    # if targetUser:
    #     assign_admin_role(targetUser['id'])
    #     print("Admin role assigned to user:", targetUser['name'])
    # else:
    #     print("No user found with such information [Note that the username and email is case sensitive].")

    app.run(debug=True)
