from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(
    __name__,
    template_folder="../Frontend/templates",
    static_folder="../Frontend/static"
)

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Psalm23:1-3",
        database="KNL_BARBERS"
    )

# ---------------- HOME ----------------
@app.route('/')
def home():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM Barber")
    barbers = cursor.fetchall()

    cursor.execute("SELECT * FROM Service")
    services = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        customers=customers,
        barbers=barbers,
        services=services
    )

# ---------------- BOOK APPOINTMENT ----------------
@app.route('/book', methods=['POST'])
def book():

    customer = request.form['customer']
    barber = request.form['barber']
    service = request.form['service']
    date = request.form['date']
    time = request.form['time']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Appointment
        (CustomerID, BarberID, ServiceID, AppointmentDate, AppointmentTime)
        VALUES (%s, %s, %s, %s, %s)
    """, (customer, barber, service, date, time))

    conn.commit()
    conn.close()

    return redirect('/appointments')

# ---------------- VIEW APPOINTMENTS ----------------
@app.route('/appointments')
def appointments():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            A.AppointmentID,
            A.AppointmentDate,
            A.AppointmentTime,
            CONCAT(C.FirstName, ' ', C.LastName) AS CustomerName,
            CONCAT(B.FirstName, ' ', B.LastName) AS BarberName,
            S.ServiceName
        FROM Appointment A
        INNER JOIN Customer C ON A.CustomerID = C.CustomerID
        INNER JOIN Barber B ON A.BarberID = B.BarberID
        INNER JOIN Service S ON A.ServiceID = S.ServiceID
    """)

    appointments = cursor.fetchall()
    conn.close()

    return render_template('appointments.html', appointments=appointments)

# ---------------- EDIT PAGE ----------------
@app.route('/edit/<int:id>')
def edit(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Appointment WHERE AppointmentID = %s", (id,))
    appointment = cursor.fetchone()

    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM Barber")
    barbers = cursor.fetchall()

    cursor.execute("SELECT * FROM Service")
    services = cursor.fetchall()

    conn.close()

    return render_template(
        'edit.html',
        appointment=appointment,
        customers=customers,
        barbers=barbers,
        services=services
    )

# ---------------- UPDATE APPOINTMENT ----------------
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    customer = request.form['customer']
    barber = request.form['barber']
    service = request.form['service']
    date = request.form['date']
    time = request.form['time']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Appointment
        SET CustomerID = %s,
            BarberID = %s,
            ServiceID = %s,
            AppointmentDate = %s,
            AppointmentTime = %s
        WHERE AppointmentID = %s
    """, (customer, barber, service, date, time, id))

    conn.commit()
    conn.close()

    return redirect('/appointments')

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)