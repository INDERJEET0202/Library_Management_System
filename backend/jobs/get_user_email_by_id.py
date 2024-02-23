import sqlite3

def get_user_email_by_id(user_id):
    conn = sqlite3.connect('database.db')  # Update with your database file path
    cursor = conn.cursor()

    cursor.execute('''
        SELECT email
        FROM users
        WHERE id = ?
    ''', (user_id,))
    user_email = cursor.fetchone()[0]

    conn.close()

    return user_email