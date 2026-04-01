<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"
const router = useRouter()
const stats = ref(null)
const error = ref(null)
const goToAppointments = () => {
  router.push("/admin/appointments")
}

const adminName = ref("")

const fetchStats = async () => {
  try {
    const token = localStorage.getItem("token")

    const response = await axios.get(
      "http://127.0.0.1:5000/api/admin/dashboard/stats",
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    stats.value = response.data
    adminName.value = response.data.admin_name || "Admin"
  } catch (err) {
    console.error(err)
    error.value = "Failed to load dashboard stats"
  }
}

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}

onMounted(() => {
  fetchStats()
})

const goToPatients = () => {
  router.push("/admin/patients")
}
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center border p-3 mb-4">
      <h4>Welcome {{ adminName }}</h4>

      <button class="btn btn-danger btn-sm"
              @click="logout">
        Logout
      </button>
    </div>

    <div v-if="error" class="text-danger mt-3">
      {{ error }}
    </div>

    <div v-if="stats" class="row mt-4">

      <div
        class="col-md-4 mb-3"
        style="cursor: pointer"
        @click="router.push('/admin/doctors')"
      >
        <div class="card p-3 shadow">
          <h5>Total Doctors</h5>
          <h3>{{ stats.total_doctors }}</h3>
        </div>
      </div>

      <div class="col-md-4 mb-3" style="cursor: pointer" @click="goToPatients">
        <div class="card p-3 shadow">
          <h5>Total Patients</h5>
          <h3>{{ stats.total_patients }}</h3>
        </div>
      </div>

      <div class="col-md-4 mb-3" style="cursor: pointer" @click="goToAppointments">
         <div class="card p-3 shadow">
          <h5>Total Appointments</h5>
          <h3>{{ stats.total_appointments }}</h3>
        </div>
      </div>

      

    </div>
  </div>
</template>