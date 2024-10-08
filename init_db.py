import sqlite3
import os
from datetime import datetime

# Function to initialize the database


def init_db(DB_NAME):
    # Check if the database exists
    db_exists = os.path.exists(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if not db_exists:
        print("Creating new database and tables...")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FLAG TEXT DEFAULT NULL
            )
        ''')

        cursor.executemany('''
            INSERT INTO menu_1 (username, password, email, role, created_at, FLAG)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [
            ('admin', 'password123', 'admin@example.com', 'admin',
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'FLAG{ADMIN_FLAG}'),
            ('guest', 'guestpassword', 'guest@example.com', 'guest',
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None),
            ('user1', 'userpassword1', 'user1@example.com', 'user',
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None),
            ('user2', 'userpassword2', 'user2@example.com', 'user',
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None),
            ('user3', 'userpassword3', 'user3@example.com', 'user',
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None)
        ])


        # Challenge 2: Vulnerable table (to SQL Injection) for taco recipes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                taco_name TEXT NOT NULL,
                tortilla_type TEXT NOT NULL,
                meat_portion INTEGER NOT NULL,
                sauce_type TEXT NOT NULL,
                secret_flag TEXT DEFAULT NULL
            )
        ''')

        # Insert sample data into menu_2 table (Taco Recipes)
        cursor.executemany('''
            INSERT INTO menu_2 (taco_name, tortilla_type, meat_portion, sauce_type, secret_flag)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            ('Classic Beef Taco', 'Soft Corn', 150, 'Mild Salsa', None),
            ('Spicy Chicken Taco', 'Hard Shell', 120, 'Spicy Salsa', None),
            ('Grilled Fish Taco', 'Flour Tortilla', 100, 'Lime Crema', None),
            ('Pork Carnitas Taco', 'Soft Corn', 200, 'Green Salsa', None),
            ('Hacker Burrito', 'Flour Tortilla', 500,
            'Chipotle Sauce', 'FLAG{HACKER_TACO_FLAG}')
        ])

        print("Database and tables created successfully.")
    else:
        print("Database already exists, skipping creation.")

    conn.commit()
    conn.close()
