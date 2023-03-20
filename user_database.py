import sqlite3
import bcrypt

def create_users_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT UNIQUE
        )
        '''
    )
    conn.commit()
    conn.close()

def check_user_credentials(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode(), hashed_password):
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user_info = cursor.fetchone()
            conn.close()
            return {
                "id": user_info[0],
                "username": user_info[1],
                "password": user_info[2],
                "email": user_info[3],
            }
    conn.close()
    return None


def get_all_usernames():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    usernames = [row[0] for row in cursor.fetchall()]

    conn.close()

    return usernames

def add_user(username, password, email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            '''
            INSERT INTO users (username, password, email) VALUES (?, ?, ?)
            ''',
            (username, hashed_password, email)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True


create_users_table()
