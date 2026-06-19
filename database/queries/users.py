# database/queries/users.py
from database.db import get_connection
import bcrypt


# This module contains functions for interacting with the users table in the database
#  such as creating new users and retrieving users by email. 

# It uses bcrypt to securely hash passwords before storing them in the database.
# Used for user registration and login functionality.
def get_user_by_email(email):
    # Connect to the database
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True means rows come back as {column: value} instead of a plain list
    print(f"Looking up user by email: {email}")  # Debug statement
    # Find the user with this email
    cursor.execute("""
        SELECT id, firstname, lastname, email, role, password_hash
        FROM users
        WHERE email = %s
    """, (email,))

    print(f"Executed query to find user by email: {email}")  # Debug statement

    
    user = None
    for row in cursor:
        user = row
        break  # We only expect one user, so we can stop after the first row

    # Always close the connection when done
    cursor.close()
    conn.close()

    return user  # Returns the user row, or None if no match


def create_user(email, password, firstname="", lastname="", role="user"):
    # Hash the password before saving — never store plain text passwords
    # bcrypt.gensalt() generates a random salt to make each hash unique
    
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),  # convert string to bytes first
        bcrypt.gensalt()
    ).decode("utf-8")  # convert bytes back to string for storing in DB

    # Connect to the database
    conn = get_connection()
    # dictionary=True is not needed here since we are only inserting data, not fetching rows
    cursor = conn.cursor() 

    # Insert the new user into the users table
    # %s are placeholders — values are passed separately to prevent SQL injection
    cursor.execute(
        "INSERT INTO users (firstname, lastname, email, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
        (firstname, lastname, email, password_hash, role)
    )

    conn.commit()  # commit() saves the changes to the database
    cursor.close()
    conn.close()


def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = None
    for row in cursor:
        user = row
        break
    
    cursor.close()
    conn.close()

    return user


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, firstname, lastname, email
        FROM users
        WHERE role != 'admin'
    """)

    users = []
    for row in cursor:
        users.append(row)

    cursor.close()
    conn.close()

    return users


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = %s
    """, (user_id,))

    conn.commit()
    cursor.close()
    conn.close()




def update_user_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    # This is the new password coming in as plain text
    # so we need to hash it before storing in the database
    new_password_hash = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute("""
        UPDATE users
        SET password_hash = %s
        WHERE id = %s
    """, (new_password_hash, user_id))

    conn.commit()
    cursor.close()
    conn.close()





