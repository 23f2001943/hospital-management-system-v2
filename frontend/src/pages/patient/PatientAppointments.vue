<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const appointments = ref([])

// FETCH
const fetchAppointments = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:5000/api/patient/appointments",
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    appointments.value = res.data.filter(a => a.status === "Booked")

  } catch (err) {
    console.error(err)
  }
}

// CANCEL
const cancelAppointment = async (id) => {
  try {
    await axios.patch(
      `http://127.0.0.1:5000/api/patient/appointment/${id}/cancel`,
      {},
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    fetchAppointments()

  } catch (err) {
    console.error(err)
  }
}

// RESCHEDULE (placeholder)
const rescheduleAppointment = (appt) => {
  alert("Reschedule coming next")
}

onMounted(fetchAppointments)
</script>

<template>
  <div class="container mt-4">

    <h2 class="mb-4">Upcoming Appointments</h2>

    <table class="table table-bordered">

      <thead>
        <tr>
          <th>Doctor</th>
          <th>Department</th>
          <th>Date</th>
          <th>Time</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="a in appointments" :key="a.appointment_id">

          <td>{{ a.doctor_name }}</td>
          <td>{{ a.department }}</td>
          <td>{{ a.date }}</td>
          <td>{{ a.time }}</td>

          <td>

            <button class="btn btn-danger btn-sm me-2"
                    @click="cancelAppointment(a.appointment_id)">
              Cancel
            </button>

            <button class="btn btn-warning btn-sm"
                    @click="rescheduleAppointment(a)">
              Reschedule
            </button>

          </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>