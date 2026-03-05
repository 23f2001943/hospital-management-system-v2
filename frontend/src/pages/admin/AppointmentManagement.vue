<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"

const appointments = ref([])
const statusFilter = ref("")

const editingAppointment = ref(null)

const editAppointment = (appt) => {
  editingAppointment.value = { ...appt }
}

const token = localStorage.getItem("token")

const fetchAppointments = async () => {

  try {

    const response = await axios.get(
      "http://localhost:5000/api/admin/appointments",
      {
        headers: {
          "Authentication-Token": token
        },
        params: {
          status: statusFilter.value || undefined
        }
      }
    )

    appointments.value = response.data

  } catch (error) {
    console.error(error)
  }

}

onMounted(() => {
  fetchAppointments()
})

const cancelAppointment = async (id) => {

  if (!confirm("Cancel this appointment?")) return

  try {

    await axios.patch(
      `http://localhost:5000/api/admin/cancel-appointment/${id}`,
      {},
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    fetchAppointments()

  } catch (error) {
    console.error(error)
  }

}

const updateAppointment = async () => {

  try {

    await axios.put(
      `http://localhost:5000/api/admin/update-appointment/${editingAppointment.value.appointment_id}`,
      editingAppointment.value,
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    editingAppointment.value = null
    fetchAppointments()

  } catch (error) {
    console.error(error)
  }

}
</script>

<template>

<div class="container mt-4">

<h2>Appointment Management</h2>

<!-- Filter -->

<div class="row mb-3">

<div class="col-md-4">

<select
v-model="statusFilter"
@change="fetchAppointments"
class="form-select"
>

<option value="">All Appointments</option>
<option value="Booked">Booked</option>
<option value="Completed">Completed</option>
<option value="Cancelled">Cancelled</option>

</select>

</div>

</div>

<!-- Table -->

<table class="table table-bordered table-hover">

<thead class="table-light">

<tr>

<th>ID</th>
<th>Doctor</th>
<th>Patient</th>
<th>Date</th>
<th>Time</th>
<th>Status</th>
<th>Action</th>

</tr>

</thead>

<tbody>

<template v-for="appt in appointments" :key="appt.appointment_id">
    <tr>
<td>{{ appt.appointment_id }}</td>
<td>{{ appt.doctor_name }}</td>
<td>{{ appt.patient_name }}</td>
<td>{{ appt.date }}</td>
<td>{{ appt.time }}</td>
<td>{{ appt.status }}</td>

<td>

<button
v-if="appt.status === 'Booked'"
class="btn btn-sm btn-warning me-2"
@click="editAppointment(appt)"
>
Edit
</button>

<button
v-if="appt.status === 'Booked'"
class="btn btn-sm btn-danger"
@click="cancelAppointment(appt.appointment_id)"
>
Cancel
</button>

</td>
</tr>

<tr v-if="editingAppointment && editingAppointment.appointment_id === appt.appointment_id">
<td colspan="7">

<div class="card p-3">

<h6>Edit Appointment</h6>

<input
v-model="editingAppointment.doctor_id"
class="form-control mb-2"
placeholder="Doctor ID"
/>

<input
v-model="editingAppointment.patient_id"
class="form-control mb-2"
placeholder="Patient ID"
/>

<input
v-model="editingAppointment.date"
type="date"
class="form-control mb-2"
/>

<input
v-model="editingAppointment.time"
type="time"
class="form-control mb-2"
/>

<button
class="btn btn-success me-2"
@click="updateAppointment"
>
Save Changes
</button>

<button
class="btn btn-secondary"
@click="editingAppointment = null"
>
Cancel
</button>

</div>

</td>
</tr>

</template>
</tbody>

</table>


</div>

</template>