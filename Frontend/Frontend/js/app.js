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


    const appointment = {


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


};