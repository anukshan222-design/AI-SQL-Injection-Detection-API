from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "models", "sqli_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

@app.route("/")
def home():
    return "SQL Injection Detection API is running!"

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({
            "error": "Please send JSON with a 'query' field"
        }), 400

    query = data["query"]

    vector = vectorizer.transform([query])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0][1]

    return jsonify({
        "query": query,
        "sql_injection": bool(prediction),
        "risk_score": round(probability * 100, 2),
        "message": "SQL Injection Detected" if prediction == 1 else "Safe Query"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)