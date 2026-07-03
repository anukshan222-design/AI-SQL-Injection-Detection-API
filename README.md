# 🛡️ AI-Powered SQL Injection Detection API

## 📌 Overview

This project is an AI-powered SQL Injection Detection API developed using Machine Learning and Flask.

The system analyzes user input in real time and predicts whether it is a normal query or a SQL Injection attack.

It is designed as an additional security layer that can be integrated into any web application.

---

## 🚀 Features

- Detects SQL Injection attacks
- REST API built using Flask
- TF-IDF Feature Extraction
- Logistic Regression Machine Learning Model
- Risk Score Prediction
- Website Integration Ready
- Easy Deployment on Render, AWS, Azure, etc.

---

## 📊 Model Performance

- Accuracy: **98.45%**
- Precision: **98-99%**
- Recall: **97-99%**
- F1 Score: **98%**

---

## 🛠 Technologies Used

- Python
- Flask
- Scikit-Learn
- Pandas
- NumPy
- Joblib
- Jupyter Notebook
- Postman

---

## 📂 Project Structure

```
SQLI_Detector/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│
├── models/
│   ├── sqli_model.pkl
│   └── vectorizer.pkl
│
└── notebook/
```

---

## ▶️ Running the Project

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-SQL-Injection-Detection-API.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the API

```bash
python app.py
```

API starts at

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoint

### POST /detect

Example Request

```json
{
    "query": "' OR 1=1 --"
}
```

Example Response

```json
{
    "query":"' OR 1=1 --",
    "sql_injection": true,
    "risk_score": 99.98,
    "message":"SQL Injection Detected"
}
```

---

## 🌐 Integration

This API can be integrated into:

- Java Spring Boot
- Java Servlets
- PHP
- React
- Node.js
- ASP.NET
- Any web application capable of sending HTTP requests

---

## 🔮 Future Improvements

- XSS Detection
- Command Injection Detection
- Path Traversal Detection
- AI-powered Web Application Firewall (WAF)
- Admin Dashboard
- Attack Logging
- Continuous Model Training

---

## 👨‍💻 Author

Amirthalingam Anukshan

BSc (Hons) Cyber Security Undergraduate

SLIIT
