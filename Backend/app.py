from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():

    return jsonify({
        "message":"KNL Barbers API Running"
    })

@app.route("/api/customers", methods=["GET"])
def get_customers():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customer")

    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(customers)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

