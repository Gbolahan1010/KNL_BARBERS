from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(
    __name__,
    template_folder="../Frontend/templates",
    static_folder="../Frontend/static"
)

@app.route('/')
def home():

    conn = get_connection()
    cursor = conn.cursor()

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

@app.route('/book', methods=['POST'])
def book():

    customer = request.form['customer']
    barber = request.form['barber']
    service = request.form['service']
    date = request.form['date']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Appointment
        (CustomerID, BarberID, ServiceID, AppointmentDate)
        VALUES (?,?,?,?)
    """,
    (customer, barber, service, date))

    conn.commit()
    conn.close()

    return redirect('/appointments')

@app.route('/appointments')
def appointments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        A.AppointmentID,
        C.FirstName + ' ' + C.LastName AS CustomerName,
        B.FirstName + ' ' + B.LastName AS BarberName,
        S.ServiceName AS ServiceName,
        A.AppointmentDate
    FROM Appointment A
    INNER JOIN Customer C
        ON A.CustomerID = C.CustomerID
    INNER JOIN Barber B
        ON A.BarberID = B.BarberID
    INNER JOIN Service S
        ON A.ServiceID = S.ServiceID
    """)

    appointments = cursor.fetchall()

    conn.close()

    return render_template(
        'appointments.html',
        appointments=appointments
    )

if __name__ == '__main__':
    app.run(debug=True)

