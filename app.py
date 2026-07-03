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