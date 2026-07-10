from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def home():
    return render_template("index.html")

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

    try:


        data = request.json



        if not data:

            return jsonify({

                "message":
                "No appointment data received"

            }),400




        conn=get_connection()

        cursor=conn.cursor()



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

            "message":
            "Appointment created successfully"

        }),201



    except Exception as e:


        return jsonify({

            "error":
            str(e)

        }),500


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

# ===============================
# UPDATE APPOINTMENT
# ===============================

@app.route("/api/appointments/<int:id>", methods=["PUT"])
def update_appointment(id):

    data = request.json


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        UPDATE Appointment

        SET

        CustomerID=%s,
        BarberID=%s,
        ServiceID=%s,
        AppointmentDate=%s,
        AppointmentTime=%s


        WHERE AppointmentID=%s

    """,

    (

        data["CustomerID"],
        data["BarberID"],
        data["ServiceID"],
        data["AppointmentDate"],
        data["AppointmentTime"],
        id

    ))


    conn.commit()

    conn.close()


    return jsonify({

        "message":"Appointment updated successfully"

    })

# ===============================
# DASHBOARD STATISTICS
# ===============================

@app.route("/api/dashboard")
def dashboard():


    conn = get_connection()

    cursor = conn.cursor(dictionary=True)


    cursor.execute(
        "SELECT COUNT(*) AS totalCustomers FROM Customer"
    )

    customers = cursor.fetchone()



    cursor.execute(
        "SELECT COUNT(*) AS totalAppointments FROM Appointment"
    )

    appointments = cursor.fetchone()



    cursor.execute(
        "SELECT COUNT(*) AS totalServices FROM Service"
    )

    services = cursor.fetchone()



    conn.close()



    return jsonify({

        "customers":
        customers["totalCustomers"],


        "appointments":
        appointments["totalAppointments"],


        "services":
        services["totalServices"]

    })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )