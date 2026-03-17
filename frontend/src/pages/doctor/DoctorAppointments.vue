<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const appointments = ref([])
const expandedId = ref(null)
const treatmentForm = ref({})

const fetchAppointments = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/api/doctor/dashboard", {
      headers: {
        "Authentication-Token": localStorage.getItem("token")
      }
    })

    appointments.value = [
      ...res.data.today,
      ...res.data.upcoming,
      ...res.data.past
    ]

  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchAppointments)

// toggle expand
const toggleView = (id) => {
  expandedId.value = expandedId.value === id ? null : id

  if (!treatmentForm.value[id]) {
    treatmentForm.value[id] = {
      diagnosis: "",
      prescription: "",
      notes: ""
    }
  }
}
// cancel appointment
const cancelAppointment = async (id) => {
  try {
    await axios.patch(
      `http://127.0.0.1:5000/api/doctor/appointment/${id}/status`,
      { status: "Cancelled" },
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
// complete appointment
const completeAppointment = async (id) => {
  try {
    await axios.patch(
      `http://127.0.0.1:5000/api/doctor/appointment/${id}/status`,
      { status: "Completed" },
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
// submit treatment
const submitTreatment = async (id) => {
  try {
    await axios.post(
      `http://127.0.0.1:5000/api/doctor/appointment/${id}/treatment`,
      treatmentForm.value[id],
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Treatment saved")
    fetchAppointments()

  } catch (err) {
    console.error(err)
  }
}

</script>
<template>
  <div class="container mt-4">

    <h2 class="mb-4">Appointments</h2>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Patient</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <template v-for="a in appointments" :key="a.appointment_id">

          <!-- MAIN ROW -->
          <tr>
            <td>{{ a.patient_name }}</td>
            <td>{{ a.date }}</td>
            <td>{{ a.time }}</td>
            <td>{{ a.status }}</td>
            <td>
            <!-- VIEW BUTTON -->
            <button class="btn btn-primary btn-sm me-2"
                    @click="toggleView(a.appointment_id)">
                {{ expandedId === a.appointment_id ? "Close" : "View" }}
            </button>

            <!-- COMPLETE -->
            <button v-if="a.status === 'Booked'"
                    class="btn btn-success btn-sm"
                    @click="completeAppointment(a.appointment_id)">
                Complete
            </button>

            <!-- CANCEL BUTTON (ONLY FOR BOOKED) -->
            <button v-if="a.status === 'Booked'"
                    class="btn btn-danger btn-sm"
                    @click="cancelAppointment(a.appointment_id)">
                Cancel
            </button>
            </td>
          </tr>

          <!-- EXPANDED CARD -->
          <tr v-if="expandedId === a.appointment_id">
            <td colspan="5">

              <div class="card p-3 shadow-sm">

                <h5>Appointment Details</h5>

                <p><b>Patient:</b> {{ a.patient_name }}</p>
                <p><b>Date:</b> {{ a.date }}</p>
                <p><b>Time:</b> {{ a.time }}</p>
                <p><b>Status:</b> {{ a.status }}</p>

                <hr>

                <!-- FORM (for Booked / Completed) -->
                <div v-if="a.status !== 'Cancelled'">

                  <div class="mb-2">
                    <label>Diagnosis</label>
                    <input v-model="treatmentForm[a.appointment_id].diagnosis"
                           class="form-control" />
                  </div>

                  <div class="mb-2">
                    <label>Prescription</label>
                    <input v-model="treatmentForm[a.appointment_id].prescription"
                           class="form-control" />
                  </div>

                  <div class="mb-2">
                    <label>Notes</label>
                    <input v-model="treatmentForm[a.appointment_id].notes"
                           class="form-control" />
                  </div>

                  <button class="btn btn-success btn-sm me-2"
                          @click="submitTreatment(a.appointment_id)">
                    Save Treatment
                  </button>

                  
                </div>

                <!-- CANCELLED -->
                <div v-else>
                  <p class="text-danger">This appointment is cancelled</p>
                </div>

              </div>

            </td>
          </tr>

        </template>
      </tbody>
    </table>

  </div>
</template>