const API = "http://localhost:5000/api";


// ===============================
// LOAD CUSTOMERS
// ===============================

async function loadCustomers(){

    const response = await fetch(`${API}/customers`);

    const customers = await response.json();


    const dropdown = document.getElementById("customer");


    dropdown.innerHTML = "";


    customers.forEach(customer => {


        dropdown.innerHTML += `

        <option value="${customer.CustomerID}">

        ${customer.FirstName} ${customer.LastName}

        </option>

        `;


    });

}



// ===============================
// LOAD BARBERS
// ===============================

async function loadBarbers(){

    const response = await fetch(`${API}/barbers`);

    const barbers = await response.json();


    const dropdown = document.getElementById("barber");


    dropdown.innerHTML="";


    barbers.forEach(barber=>{


        dropdown.innerHTML += `

        <option value="${barber.BarberID}">

        ${barber.FirstName} ${barber.LastName}

        </option>

        `;


    });

}



// ===============================
// LOAD SERVICES
// ===============================


async function loadServices(){

    const response = await fetch(`${API}/services`);

    const services = await response.json();


    const dropdown=document.getElementById("service");


    dropdown.innerHTML="";


    services.forEach(service=>{


        dropdown.innerHTML +=`

        <option value="${service.ServiceID}">

        ${service.ServiceName}

        (€${service.Price})

        </option>

        `;


    });


}



// ===============================
// CREATE APPOINTMENT
// ===============================


async function bookAppointment(){


    const customer =
    document.getElementById("customer").value;


    const barber =
    document.getElementById("barber").value;


    const service =
    document.getElementById("service").value;


    const date =
    document.getElementById("date").value;


    const time =
    document.getElementById("time").value;



    // ==========================
    // VALIDATION
    // ==========================


    if(
        customer === "" ||
        barber === "" ||
        service === "" ||
        date === "" ||
        time === ""
    ){

        alert(
        "Please complete all fields before booking"
        );

        return;

    }



    // Prevent past dates

    let selectedDate =
    new Date(date);


    let today =
    new Date();


    today.setHours(0,0,0,0);



    if(selectedDate < today){


        alert(
        "You cannot book an appointment in the past"
        );


        return;


    }




    const appointment = {


        CustomerID: customer,

        BarberID: barber,

        ServiceID: service,

        AppointmentDate: date,

        AppointmentTime: time


    };




    try{


        const response = await fetch(

            `${API}/appointments`,

            {


            method:"POST",


            headers:{

                "Content-Type":
                "application/json"

            },


            body:
            JSON.stringify(appointment)


            }

        );



        const result =
        await response.json();



        alert(result.message);



        loadAppointments();

        loadDashboard();



    }


    catch(error){


        console.error(error);


        alert(
        "Unable to create appointment"
        );


    }


}



    const response = await fetch(
        `${API}/appointments`,
        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },


            body:
            JSON.stringify(appointment)

        }
    );



    const result = await response.json();


    alert(result.message);



    loadAppointments();



}



// ===============================
// LOAD APPOINTMENTS TABLE
// ===============================


async function loadAppointments(){


    const response =
    await fetch(`${API}/appointments`);


    const appointments =
    await response.json();



    const table =
    document.getElementById("appointmentTable");



    table.innerHTML="";



    appointments.forEach(a=>{


        table.innerHTML +=`

        <tr>

        <td>${a.AppointmentID}</td>

        <td>${a.CustomerName}</td>

        <td>${a.BarberName}</td>

        <td>${a.ServiceName}</td>

        <td>${a.AppointmentDate}</td>

        <td>${a.AppointmentTime}</td>

        <td>


<button

class="edit-btn"

onclick="editAppointment(${a.AppointmentID})">

Edit

</button>



<button

class="delete-btn"

onclick="deleteAppointment(${a.AppointmentID})">

Delete

</button>


</td>


        </tr>


        `;


    });


}



// ===============================
// DELETE APPOINTMENT
// ===============================


async function deleteAppointment(id){


    if(confirm("Delete this appointment?")){


        await fetch(

            `${API}/appointments/${id}`,

            {
                method:"DELETE"
            }

        );


        loadAppointments();


    }


}





// ===============================
// START APPLICATION
// ===============================


window.onload=function(){


    loadCustomers();

    loadBarbers();

    loadServices();

    loadAppointments();

    loadDashboard();


};

// ===============================
// EDIT APPOINTMENT
// ===============================


async function editAppointment(id){


    const response =
    await fetch(`${API}/appointments`);


    const appointments =
    await response.json();



    const appointment =
    appointments.find(
        a=>a.AppointmentID===id
    );



    document.getElementById("customer").value =
    appointment.CustomerID;



    document.getElementById("barber").value =
    appointment.BarberID;



    document.getElementById("service").value =
    appointment.ServiceID;



    document.getElementById("date").value =
    appointment.AppointmentDate;



    document.getElementById("time").value =
    appointment.AppointmentTime;



    document.getElementById("bookingButton").innerHTML =
    "Update Appointment";



    document.getElementById("bookingButton").onclick =
    function(){

        updateAppointment(id);

    };


}

async function updateAppointment(id){


    const appointment={


        CustomerID:
        document.getElementById("customer").value,


        BarberID:
        document.getElementById("barber").value,


        ServiceID:
        document.getElementById("service").value,


        AppointmentDate:
        document.getElementById("date").value,


        AppointmentTime:
        document.getElementById("time").value


    };



    await fetch(

        `${API}/appointments/${id}`,

        {

            method:"PUT",


            headers:{

                "Content-Type":
                "application/json"

            },


            body:
            JSON.stringify(appointment)

        }

    );



    alert(
        "Appointment updated successfully"
    );


    loadAppointments();



}