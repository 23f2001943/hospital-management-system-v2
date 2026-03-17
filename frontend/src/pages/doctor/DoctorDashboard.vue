<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

// state
const todayAppointments = ref([])
const upcomingAppointments = ref([])
const pastAppointments = ref([])

const router = useRouter()

// fetch dashboard data
const fetchDashboard = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/api/doctor/dashboard", {
      headers: {
        "Authentication-Token": localStorage.getItem("token")
      }
    })

    todayAppointments.value = res.data.today
    upcomingAppointments.value = res.data.upcoming
    pastAppointments.value = res.data.past

  } catch (err) {
    console.error(err)
  }
}

// update appointment status
const updateStatus = async (id, status) => {
  try {
    await axios.patch(
      `http://127.0.0.1:5000/api/doctor/appointment/${id}/status`,
      { status },
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    fetchDashboard()

  } catch (err) {
    console.error(err)
  }
}

// navigation functions
const goToAppointments = () => {
  router.push("/doctor/appointments")
}

const goToPatients = () => {
  router.push("/doctor/patients")
}

const goToAvailability = () => {
  router.push("/doctor/availability") // create later
}

// computed values

// total appointments
const totalAppointments = computed(() => {
  let count = 0

  const all = [
    ...todayAppointments.value,
    ...upcomingAppointments.value,
    ...pastAppointments.value
  ]

  all.forEach(a => {
    if (a.status === "Booked") {
      count++
    }
  })

  return count
})

// unique patients count
const uniquePatientsCount = computed(() => {
  const ids = new Set()

  todayAppointments.value.forEach(a => ids.add(a.patient_name))
  upcomingAppointments.value.forEach(a => ids.add(a.patient_name))
  pastAppointments.value.forEach(a => ids.add(a.patient_name))

  return ids.size
})

// lifecycle
onMounted(fetchDashboard)
</script>

<template>
  <div class="container mt-4">

    <h2 class="mb-4">Doctor Dashboard</h2>

    <!-- SUMMARY CARDS -->
    <div class="row mb-4">

  <!-- APPOINTMENTS -->
  <div class="col-md-4">
    <div class="card p-3 shadow-sm cursor-pointer"
         @click="goToAppointments">
      <h5>Appointments</h5>
      <h2>{{ totalAppointments }}</h2>
    </div>
  </div>

  <!-- PATIENTS -->
  <div class="col-md-4">
    <div class="card p-3 shadow-sm cursor-pointer"
         @click="goToPatients">
      <h5>My Patients</h5>
      <h2>{{ uniquePatientsCount }}</h2>
    </div>
  </div>

  <!-- AVAILABILITY -->
  <div class="col-md-4">
    <div class="card p-3 shadow-sm cursor-pointer"
         @click="goToAvailability">
      <h5>My Availability</h5>
      <h2>Edit</h2>
    </div>
  </div>

</div>

    <!-- TODAY -->
    <div class="card p-3 mb-4 shadow-sm">
      <h4>Today's Appointments</h4>

      <div v-if="todayAppointments.length === 0">No appointments today</div>

      <div v-for="appt in todayAppointments" :key="appt.appointment_id" class="border p-2 mb-2 rounded">
        <p><b>Patient:</b> {{ appt.patient_name }}</p>
        <p><b>Time:</b> {{ appt.time }}</p>
        <p><b>Status:</b> {{ appt.status }}</p>

        <button @click="updateStatus(appt.appointment_id, 'Completed')" class="btn btn-success btn-sm me-2">
          Complete
        </button>
        <button @click="updateStatus(appt.appointment_id, 'Cancelled')" class="btn btn-danger btn-sm">
          Cancel
        </button>
      </div>
    </div>

    
  </div>
</template>