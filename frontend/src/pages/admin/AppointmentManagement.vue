<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"

const appointments = ref([])
const statusFilter = ref("")
const viewingHistory = ref(null)
const patientHistory = ref([])
const editingAppointment = ref(null)
const appointmentCount = computed(() => appointments.value.length)

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

const viewHistory = async (appt) => {

  if (viewingHistory.value === appt.appointment_id) {
    viewingHistory.value = null
    return
  }

  try {

    const response = await axios.get(
      `http://localhost:5000/api/admin/patient-history/${appt.patient_id}`,
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    patientHistory.value = response.data
    viewingHistory.value = appt.appointment_id

  } catch (error) {
    console.error(error)
  }
}
</script>

<template>

<div class="container mt-4">

<div class="d-flex justify-content-between align-items-center mb-3">

<h2>Appointment Management</h2>

<span class="badge bg-primary fs-6">
Total: {{ appointmentCount }}
</span>

</div>

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
class="btn btn-sm btn-info me-2"
@click="viewHistory(appt)"
>
View History
</button>

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
<tr v-if="viewingHistory === appt.appointment_id">
<td colspan="7">

<div class="card p-3">

<h6>Patient History</h6>

<table class="table table-sm table-bordered">

<thead>
<tr>
<th>Appointment ID</th>
<th>Doctor</th>
<th>Department</th>
<th>Date</th>
<th>Time</th>
<th>Status</th>
<th>Diagnosis</th>
<th>Prescription</th>
<th>Notes</th>
</tr>
</thead>

<tbody>

<tr v-for="h in patientHistory" :key="h.appointment_id">

<td>{{ h.appointment_id }}</td>
<td>{{ h.doctor_name }}</td>
<td>{{ h.department }}</td>
<td>{{ h.date }}</td>
<td>{{ h.time }}</td>
<td>{{ h.status }}</td>
<td>{{ h.diagnosis || "-" }}</td>
<td>{{ h.prescription || "-" }}</td>
<td>{{ h.notes || "-" }}</td>

</tr>

</tbody>

</table>

<button
class="btn btn-secondary"
@click="viewingHistory = null"
>
Close
</button>

</div>

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