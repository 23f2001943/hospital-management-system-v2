<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"


const taskId = ref(null)
const filePath = ref(null)
const exportStatus = ref("idle") // idle | processing | done
// STATE
const profile = ref({})
const editMode = ref(false)

const showCompleted = ref(false)
const completedAppointments = ref([])

import { useRouter } from "vue-router"
const router = useRouter()

const goToDoctors = () => {
  router.push("/patient/doctors")
}

const goToAppointments = () => {
  router.push("/patient/appointments")
}

const goToHistory = () => {
  router.push("/patient/history")
}

// ================= FETCH PROFILE =================
const fetchProfile = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:5000/api/patient/profile",
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    profile.value = res.data

  } catch (err) {
    console.error(err)
  }
}

const fetchCompletedAppointments = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:5000/api/patient/history/completed",
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    completedAppointments.value = res.data

  } catch (err) {
    console.error(err)
  }
}

const openCompleted = () => {
  showCompleted.value = true
  fetchCompletedAppointments()
}

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}

// ================= UPDATE PROFILE =================
const updateProfile = async () => {
  try {
    await axios.put(
      "http://127.0.0.1:5000/api/patient/profile",
      profile.value,
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Profile updated")
    editMode.value = false

  } catch (err) {
    console.error(err)
  }
}

// ==== LIFECYCLE ==========
// EXPORT HISTORY
const exportHistory = async () => {
  try {
    const res = await axios.post(
      "http://127.0.0.1:5000/api/patient/export-history",
      {},
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    taskId.value = res.data.task_id
    exportStatus.value = "processing"

    checkStatus()

  } catch (err) {
    console.error(err)
  }
}
// polling function to check status of export task
const checkStatus = () => {
  const interval = setInterval(async () => {

    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/api/patient/export-status/${taskId.value}`,
        {
          headers: {
            "Authentication-Token": localStorage.getItem("token")
          }
        }
      )

      if (res.data.status === "completed") {
        filePath.value = res.data.file
        exportStatus.value = "done"
        clearInterval(interval)
      }

    } catch (err) {
      console.error(err)
      clearInterval(interval)
    }

  }, 2000)
}


const downloadFile = async () => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:5000/api/patient/download-file?path=${filePath.value}`,
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        },
        responseType: "blob"
      }
    )

    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement("a")
    link.href = url
    link.setAttribute("download", "history.csv")
    document.body.appendChild(link)
    link.click()

  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchProfile)
</script>

<template>
  <div class="container mt-4">

    <!--  NAVBAR -->
    <div class="d-flex justify-content-between align-items-center border p-3 mb-4">
      <h4>Welcome {{ profile.name }}</h4>

      <div>
        <button class="btn btn-success btn-sm me-2"
                @click="openCompleted">
          Completed Appointments
        </button>

        <button class="btn btn-primary btn-sm me-2"
                @click="editMode = !editMode">
          Edit Profile
        </button>

        <button class="btn btn-danger btn-ms"
                @click="logout">
          Logout
        </button>

      </div>
    </div>

    <!-- EXPORT BUTTON -->
    <div class="mb-3">

      <!-- Idle -->
      <button v-if="exportStatus === 'idle'"
              class="btn btn-dark"
              @click="exportHistory">
        Export History
      </button>

      <!-- Processing -->
      <button v-if="exportStatus === 'processing'"
              class="btn btn-warning"
              disabled>
        Processing...
      </button>

      <!-- Done -->
      <button v-if="exportStatus === 'done'"
              class="btn btn-success"
              @click="downloadFile">
        Download History
      </button>

    </div>

    <div class="row mb-4">

      <div class="col-md-4">
        <div class="card p-3 shadow-sm cursor-pointer"
            @click="goToDoctors">
          <h5>Doctors</h5>
          <h3>View</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 shadow-sm cursor-pointer"
            @click="goToAppointments">
          <h5>Upcoming Appointments</h5>
          <h3>View</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 shadow-sm cursor-pointer"
            @click="goToHistory">
          <h5>Past Appointments</h5>
          <h3>View</h3>
        </div>
      </div>

    </div>
   <!---history of completed appointments-->
    <div v-if="showCompleted" class="card p-4 shadow mt-3 position-relative">

  <!-- CLOSE -->
  <button class="btn btn-sm btn-danger position-absolute"
          style="top: 10px; right: 10px;"
          @click="showCompleted = false">
    ✖
  </button>

  <h4 class="mb-3 text-success">Completed Appointments</h4>

  <div v-if="completedAppointments.length === 0" class="text-muted">
    No completed appointments yet.
  </div>

  <table v-else class="table table-bordered">

    <thead class="table-light">
      <tr>
        <th>Doctor</th>
        <th>Date</th>
        <th>Time</th>
        <th>Diagnosis</th>
        <th>Prescription</th>
        <th>Notes</th>
      </tr>
    </thead>

    <tbody>

      <tr v-for="c in completedAppointments" :key="c.date + c.time">

        <td>{{ c.doctor_name }}</td>
        <td>{{ c.date }}</td>

        <td>
          {{ c.time === '09:00' ? '08:00 - 12:00' : '16:00 - 21:00' }}
        </td>

        <td>{{ c.diagnosis || '-' }}</td>
        <td>{{ c.prescription || '-' }}</td>
        <td>{{ c.notes || '-' }}</td>

      </tr>

    </tbody>

  </table>

</div>

    <!--  EDIT PROFILE BOX -->
    <div v-if="editMode" class="card p-4 shadow-sm">

      <h5 class="mb-3">Edit Profile</h5>

      <!-- NAME -->
      <div class="mb-2">
        <label>Name</label>
        <input v-model="profile.name" class="form-control" />
      </div>

      <!-- GENDER -->
      <div class="mb-2">
        <label>Gender</label>
        <select v-model="profile.gender" class="form-control">
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>

      <!-- BLOOD GROUP -->
      <div class="mb-2">
        <label>Blood Group</label>
        <input v-model="profile.blood_group" class="form-control" />
      </div>

      <!-- CONTACT -->
      <div class="mb-2">
        <label>Contact Number</label>
        <input v-model="profile.contact_number" class="form-control" />
      </div>

      <!-- EMERGENCY CONTACT -->
      <div class="mb-2">
        <label>Emergency Contact</label>
        <input v-model="profile.emergency_contact" class="form-control" />
      </div>

      <!-- ADDRESS -->
      <div class="mb-2">
        <label>Address</label>
        <textarea v-model="profile.address" class="form-control"></textarea>
      </div>

      <!-- DOB -->
      <div class="mb-3">
        <label>Date of Birth</label>
        <input type="date" v-model="profile.date_of_birth" class="form-control" />
      </div>

      <!-- ACTION BUTTONS -->
      <div class="d-flex justify-content-between mt-3">

        <button class="btn btn-success btn-sm"
                @click="updateProfile">
          Save
        </button>

        <button class="btn btn-secondary btn-sm"
                @click="editMode = false">
          Cancel
        </button>

      </div>

    </div>

  </div>
</template>