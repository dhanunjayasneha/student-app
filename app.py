from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/")
def home():
    return "Student App Running!"

@app.route("/add", methods=["POST"])
def add_student():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (id, name, grade) VALUES (%s, %s, %s)",
        (data["id"], data["name"], data["grade"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"})

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
