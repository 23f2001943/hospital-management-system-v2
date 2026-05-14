<script setup>
import { ref, onMounted, computed } from "vue"
import API from "../../api";
import { useRouter } from "vue-router"

// state
const todayAppointments = ref([])
const upcomingAppointments = ref([])
const pastAppointments = ref([])

const router = useRouter()

const showAvailability = ref(false)
const goToAvailability = () => {
  showAvailability.value = !showAvailability.value
}
const availability = ref([])

const expandedId = ref(null)
const treatmentForm = ref({})

const doctorName = ref("")

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}

const toggleView = (id, appt) => {
  expandedId.value = expandedId.value === id ? null : id

  if (!treatmentForm.value[id]) {
    treatmentForm.value[id] = {
      diagnosis: appt.diagnosis || "",
      prescription: appt.prescription || "",
      notes: appt.notes || ""
    }
  }
}

const submitTreatment = async (id) => {
  try {
    await API.post(
      `/api/doctor/appointment/${id}/treatment`,
      treatmentForm.value[id],
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Treatment saved")
    fetchDashboard()

  } catch (err) {
    console.error(err)
  }
}

// generate next 7 days
const generateDates = () => {
  const today = new Date()

  for (let i = 0; i < 7; i++) {
    const d = new Date()
    d.setDate(today.getDate() + i)

    const formatted = d.toISOString().split("T")[0]

    availability.value.push({
      date: formatted,
      morning: false,
      evening: false
    })
  }
}

const saveAvailability = async () => {
  try {
    await API.put(
      "/api/doctor/availability",
      { availability: availability.value },
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Availability saved!")
     showAvailability.value = false

  } catch (err) {
    console.error(err)
  }
}
// fetch dashboard data
const fetchDashboard = async () => {
  try {
    const res = await API.get("/api/doctor/dashboard", {
      headers: {
        "Authentication-Token": localStorage.getItem("token")
      }
    })

    todayAppointments.value = res.data.today
    upcomingAppointments.value = res.data.upcoming
    pastAppointments.value = res.data.past

    doctorName.value = res.data.doctor_name || "Doctor"


  } catch (err) {
    console.error(err)
  }
}

// update appointment status
const updateStatus = async (id, status) => {
  try {
    await API.patch(
      `/api/doctor/appointment/${id}/status`,
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
onMounted(() => {
  fetchDashboard()
  generateDates()
})
</script>

<template>
  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center border p-3 mb-4">
    <h4>Welcome Dr. {{ doctorName }}</h4>

    <button class="btn btn-danger btn-sm"
            @click="logout">
      Logout
    </button>
  </div>

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

<div v-if="showAvailability" class="card p-4 shadow-sm mb-4">

  <h4 class="mb-3">Doctor Availability (Next 7 Days)</h4>

  <div v-for="day in availability" :key="day.date"
       class="d-flex align-items-center mb-3">

    <!-- DATE -->
    <div style="width: 150px;">
      <b>{{ day.date }}</b>
    </div>

    <!-- MORNING SLOT -->
    <button class="btn me-3"
            :class="day.morning ? 'btn-success' : 'btn-outline-secondary'"
            @click="day.morning = !day.morning">
      08:00 - 12:00
    </button>

    <!-- EVENING SLOT -->
    <button class="btn"
            :class="day.evening ? 'btn-success' : 'btn-outline-secondary'"
            @click="day.evening = !day.evening">
      16:00 - 21:00
    </button>

  </div>

  <button class="btn btn-primary mt-3" @click="saveAvailability">
    Save Availability
  </button>

</div>

    <!-- TODAY -->
    <div class="card p-3 mb-4 shadow-sm">
      <h4>Today's Appointments</h4>

      <div v-if="todayAppointments.length === 0">No appointments today</div>

      <template v-for="appt in todayAppointments" :key="appt.appointment_id">

        <!-- MAIN CARD -->
        <div class="border p-2 mb-2 rounded">

          <p><b>Patient:</b> {{ appt.patient_name }}</p>
          <p><b>Time:</b> {{ appt.time }}</p>
          <p><b>Status:</b> {{ appt.status }}</p>

          <!-- ACTIONS -->
          <button class="btn btn-primary btn-sm me-2"
                  @click="toggleView(appt.appointment_id, appt)">
            {{ expandedId === appt.appointment_id ? "Close" : "View" }}
          </button>

          

          <button @click="updateStatus(appt.appointment_id, 'Cancelled')"
                  class="btn btn-danger btn-sm"
                  v-if="appt.status === 'Booked'">
            Cancel
          </button>

        </div>

        <!--  EXPANDED VIEW -->
        <div v-if="expandedId === appt.appointment_id"
            class="card p-3 mb-3 shadow-sm">

          <h5>Appointment Details</h5>

          <p><b>Patient:</b> {{ appt.patient_name }}</p>
          <p><b>Date:</b> {{ appt.date }}</p>
          <p><b>Time:</b> {{ appt.time }}</p>
          <p><b>Status:</b> {{ appt.status }}</p>

          <hr>

          <div v-if="appt.status !== 'Cancelled'">

            <div class="mb-2">
              <label>Diagnosis</label>
              <input v-model="treatmentForm[appt.appointment_id].diagnosis"
                    class="form-control" />
            </div>

            <div class="mb-2">
              <label>Prescription</label>
              <input v-model="treatmentForm[appt.appointment_id].prescription"
                    class="form-control" />
            </div>

            <div class="mb-2">
              <label>Notes</label>
              <input v-model="treatmentForm[appt.appointment_id].notes"
                    class="form-control" />
            </div>

            <button class="btn btn-success btn-sm"
                    @click="submitTreatment(appt.appointment_id)">
              Save Treatment
            </button>

          </div>

          <div v-else>
            <p class="text-danger">This appointment is cancelled</p>
          </div>

        </div>

      </template>
    </div>

    
  </div>
</template>
