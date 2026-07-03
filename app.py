from flask import Flask, request, jsonify
import joblib
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "models", "sqli_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        ssl_disabled=False
    )

def save_attempt(username, password_input, combined_input, sql_injection, risk_score, message, ip_address):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO login_attempts
        (username, password_input, combined_input, sql_injection, risk_score, message, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            username,
            password_input,
            combined_input,
            sql_injection,
            risk_score,
            message,
            ip_address
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print("Database insert error:", e)

@app.route("/")
def home():
    return "SQL Injection Detection API with MySQL logging is running!"

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({
            "error": "Please send JSON with 'username' and 'password' fields"
        }), 400

    username = data["username"]
    password_input = data["password"]

    combined_input = f"{username} {password_input}"

    vector = vectorizer.transform([combined_input])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0][1]

    sql_injection = bool(prediction)
    risk_score = round(probability * 100, 2)
    message = "SQL Injection Detected" if prediction == 1 else "Safe Query"
    ip_address = request.remote_addr

    save_attempt(
        username,
        password_input,
        combined_input,
        sql_injection,
        risk_score,
        message,
        ip_address
    )

    return jsonify({
        "username": username,
        "password": password_input,
        "combined_input": combined_input,
        "sql_injection": sql_injection,
        "risk_score": risk_score,
        "message": message
    })

@app.route("/attempts", methods=["GET"])
def attempts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, username, password_input, sql_injection, risk_score, message, ip_address, created_at
            FROM login_attempts
            ORDER BY id DESC
            LIMIT 20
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/demo-detect", methods=["POST"])
def demo_detect():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({
            "error": "Please send JSON with 'username' and 'password'"
        }), 400

    username = data["username"]
    password_input = data["password"]

    combined_input = f"{username} {password_input}"

    vector = vectorizer.transform([combined_input])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0][1]

    return jsonify({
        "username": username,
        "password": password_input,
        "combined_input": combined_input,
        "sql_injection": bool(prediction),
        "risk_score": round(probability * 100, 2),
        "message": "SQL Injection Detected" if prediction == 1 else "Safe Query",
        "stored_in_database": False
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)