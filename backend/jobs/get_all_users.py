import sqlite3
from datetime import datetime, timedelta

def get_inactive_users():
    conn = sqlite3.connect('./database/database.db')
    cursor = conn.cursor()

    # Calculate the datetime one minute ago
    one_minute_ago = datetime.now() - timedelta(minutes=1)

    cursor.execute('SELECT name, email FROM users WHERE last_visited < ?', (one_minute_ago,))
    inactive_users = cursor.fetchall()

    conn.close()
    
    return inactive_users
