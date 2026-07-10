const API = "/api";


// ===============================
// LOAD CUSTOMERS
// ===============================

async function loadCustomers(){

    try {

        const response = await fetch(`${API}/customers`);

        const customers = await response.json();

        const dropdown = document.getElementById("customer");

        dropdown.innerHTML =
        `<option value="">Select Customer</option>`;


        customers.forEach(customer => {

            dropdown.innerHTML += `
                <option value="${customer.CustomerID}">
                    ${customer.FirstName} ${customer.LastName}
                </option>
            `;

        });

    }

    catch(error){

        console.error("Customer loading error:", error);

    }

}



// ===============================
// LOAD BARBERS
// ===============================

async function loadBarbers(){

    try{

        const response = await fetch(`${API}/barbers`);

        const barbers = await response.json();


        const dropdown =
        document.getElementById("barber");


        dropdown.innerHTML =
        `<option value="">Select Barber</option>`;


        barbers.forEach(barber=>{


            dropdown.innerHTML +=`

                <option value="${barber.BarberID}">
                    ${barber.FirstName} ${barber.LastName}
                </option>

            `;


        });


    }

    catch(error){

        console.error("Barber loading error:",error);

    }

}



// ===============================
// LOAD SERVICES
// ===============================

async function loadServices(){

    try{


        const response =
        await fetch(`${API}/services`);


        const services =
        await response.json();



        const dropdown =
        document.getElementById("service");



        dropdown.innerHTML =
        `<option value="">Select Service</option>`;



        services.forEach(service=>{


            dropdown.innerHTML +=`

                <option value="${service.ServiceID}">
                    ${service.ServiceName} (€${service.Price})
                </option>

            `;


        });


    }


    catch(error){

        console.error("Service loading error:",error);

    }

}




// ===============================
// CREATE APPOINTMENT
// ===============================

async function bookAppointment(){


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



    if(
        appointment.CustomerID==="" ||
        appointment.BarberID==="" ||
        appointment.ServiceID==="" ||
        appointment.AppointmentDate==="" ||
        appointment.AppointmentTime===""
    ){

        alert("Please complete all fields");

        return;

    }



    try{


        const response =
        await fetch(

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


        alert("Unable to create appointment");


    }


}




// ===============================
// LOAD APPOINTMENTS
// ===============================

async function loadAppointments(){


    try{


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


                <button onclick="editAppointment(${a.AppointmentID})">
                    Edit
                </button>


                <button onclick="deleteAppointment(${a.AppointmentID})">
                    Delete
                </button>


                </td>


            </tr>


            `;


        });


    }


    catch(error){

        console.error(error);

    }


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
// EDIT APPOINTMENT
// ===============================

async function editAppointment(id){


    const response =
    await fetch(`${API}/appointments`);



    const appointments =
    await response.json();



    const a =
    appointments.find(
        x=>x.AppointmentID===id
    );



    document.getElementById("customer").value =
    a.CustomerID;


    document.getElementById("barber").value =
    a.BarberID;


    document.getElementById("service").value =
    a.ServiceID;


    document.getElementById("date").value =
    a.AppointmentDate;


    document.getElementById("time").value =
    a.AppointmentTime;


}




// ===============================
// UPDATE APPOINTMENT
// ===============================

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


    alert("Appointment updated successfully");


    loadAppointments();


}





// ===============================
// START APPLICATION
// ===============================

window.onload=function(){


    loadCustomers();

    loadBarbers();

    loadServices();

    loadAppointments();


};