from flask import Blueprint, request, jsonify
from utils.auth_utils import hash_password, check_password, generate_token
import mysql.connector
from mysql.connector import IntegrityError

auth = Blueprint('auth', __name__)

# Function to get a MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='chatbot_db'
    )

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username, password = data.get("username"), data.get("password")
    password_hash = hash_password(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Signup successful"}), 201
    except IntegrityError:
        return jsonify({"error": "Username already exists"}), 409


@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username, password = data.get("username"), data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, password_hash FROM users WHERE username = %s",
        (username,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row and check_password(password, row[1]):
        token = generate_token(row[0])
        return jsonify({"token": token, "user_id": row[0]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
