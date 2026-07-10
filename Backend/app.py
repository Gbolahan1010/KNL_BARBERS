from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection


app = Flask(__name__)

CORS(app)


@app.route("/")
def home():

    return jsonify({
        "message": "KNL Barbers API Running"
    })


@app.route("/api/customers")
def get_customers():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customer")

    customers = cursor.fetchall()

    conn.close()

    return jsonify(customers)



@app.route("/api/barbers")
def get_barbers():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Barber")

    barbers = cursor.fetchall()

    conn.close()

    return jsonify(barbers)



@app.route("/api/services")
def get_services():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Service")

    services = cursor.fetchall()

    conn.close()

    return jsonify(services)



@app.route("/api/appointments")
def get_appointments():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            A.AppointmentID,
            CONCAT(C.FirstName,' ',C.LastName) AS CustomerName,
            CONCAT(B.FirstName,' ',B.LastName) AS BarberName,
            S.ServiceName,
            A.AppointmentDate,
            A.AppointmentTime

        FROM Appointment A

        INNER JOIN Customer C
        ON A.CustomerID = C.CustomerID

        INNER JOIN Barber B
        ON A.BarberID = B.BarberID

        INNER JOIN Service S
        ON A.ServiceID = S.ServiceID

    """)


    appointments = cursor.fetchall()


# Convert MySQL TIME object to string
    for appointment in appointments:

        if appointment["AppointmentTime"]:
            appointment["AppointmentTime"] = str(
                appointment["AppointmentTime"]
            )


    conn.close()


    return jsonify(appointments)




@app.route("/api/appointments", methods=["POST"])
def create_appointment():

    data = request.json


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO Appointment
        (
            CustomerID,
            BarberID,
            ServiceID,
            AppointmentDate,
            AppointmentTime
        )

        VALUES (%s,%s,%s,%s,%s)

    """,
    (
        data["CustomerID"],
        data["BarberID"],
        data["ServiceID"],
        data["AppointmentDate"],
        data["AppointmentTime"]
    ))


    conn.commit()

    conn.close()


    return jsonify({
        "message":"Appointment created"
    })



@app.route("/api/appointments/<int:id>", methods=["DELETE"])
def delete_appointment(id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM Appointment
        WHERE AppointmentID=%s
        """,
        (id,)
    )


    conn.commit()

    conn.close()


    return jsonify({
        "message":"Appointment deleted"
    })



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )